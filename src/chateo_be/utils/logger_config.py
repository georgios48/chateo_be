import gzip
import logging
import logging.handlers
import os
import shutil
import tempfile
from pathlib import Path
from typing import Final


class LoggerConfig:
    _LOG_FMT: Final[str] = "%(asctime)s - %(levelname)s - %(message)s"
    _COPY_BUFSIZE: Final[int] = 1024 * 1024  # 1 MiB

    @staticmethod
    def _gzip_namer(path: str) -> str:
        """Ensure rotated log files end with .gz."""
        return path if path.endswith(".gz") else f"{path}.gz"

    @classmethod
    def _gzip_rotator(cls, source: str, dest: str) -> None:
        """
        Compress `source` -> `dest` atomically, then remove `source`.

        Atomic replace avoids leaving partial .gz files on crashes.
        """
        dest_path = Path(dest)
        dest_dir = dest_path.parent if dest_path.parent != Path("") else Path(".")

        fd, tmp = tempfile.mkstemp(prefix=".logrotate-", suffix=".gz", dir=str(dest_dir))
        tmp_path = Path(tmp)

        try:
            os.close(fd)
            with open(source, "rb") as f_in, gzip.open(tmp_path, "wb", compresslevel=6) as f_out:
                shutil.copyfileobj(f_in, f_out, length=cls._COPY_BUFSIZE)

            os.replace(tmp_path, dest)  # atomic on same filesystem
            tmp_path = None  # ownership transferred to dest
            os.remove(source)
        finally:
            if tmp_path is not None:
                try:
                    tmp_path.unlink()
                except FileNotFoundError:
                    pass

    @classmethod
    def setup_logger(
        cls,
        name: str = "chateo",
        level: int = logging.INFO,
        log_file: str = "logs/chateo.log",
        backup_count: int = 365,
        when: str = "midnight",
        interval: int = 1,
    ) -> logging.Logger:
        """Setup logger with timed rotation + gzip compression."""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False  # avoid duplicate logs via root/parent handlers

        if logger.handlers:  # already configured
            return logger

        formatter = logging.Formatter(cls._LOG_FMT)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        log_path = Path(log_file)
        if log_path.parent != Path("."):
            log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=str(log_path),
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding="utf-8",
            errors="backslashreplace",
            delay=True,
        )
        file_handler.setLevel(level)
        file_handler.suffix = "%Y-%m-%d"
        file_handler.namer = cls._gzip_namer
        file_handler.rotator = cls._gzip_rotator
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger
