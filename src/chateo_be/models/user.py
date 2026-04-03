import bcrypt
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    phone_number = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    pin_hash = Column(String, nullable=False)

    # --- PIN VALIDATION ---
    @staticmethod
    def _validate_pin(pin: str):
        if not pin.isdigit() or len(pin) != 4:
            raise ValueError("PIN must be exactly 4 digits")

    # --- SET PIN (hash it) ---
    def set_pin(self, pin: str):
        self._validate_pin(pin)
        salt = bcrypt.gensalt()
        self.pin_hash = bcrypt.hashpw(pin.encode(), salt).decode()

    # --- CHECK PIN ---
    def check_pin(self, pin: str) -> bool:
        self._validate_pin(pin)
        return bcrypt.checkpw(pin.encode(), self.pin_hash.encode())

    def __repr__(self):
        return f"<User(phone_number={self.phone_number}, name={self.first_name} {self.last_name})>"
