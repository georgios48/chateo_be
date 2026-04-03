from typing import Any, ClassVar, Set
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from src.chateo_be.utils.validations import not_empty


class TrimModel(BaseModel):
    # ClassVar: not a model field (Pydantic v2 treats leading-_ names as private attrs).
    trim_exclude_fields: ClassVar[Set[str]] = set()

    @field_validator("*", mode="before")
    @classmethod
    def trim_strings(cls, v: Any, info):
        if isinstance(v, str):
            name = info.field_name
            if name not in cls.trim_exclude_fields:
                v = v.strip()
                if not not_empty(v):
                    raise ValueError(f"{name} cannot be empty")
            elif not v:
                raise ValueError(f"{name} cannot be empty")
        return v


class DoesPhoneNumberExistRequest(TrimModel):
    phone_number: str


class CreateUserRequest(TrimModel):
    trim_exclude_fields: ClassVar[Set[str]] = {"last_name"}

    phone_number: str
    first_name: str
    last_name: str
    pin: str

    @field_validator("pin")
    @classmethod
    def pin_four_digits(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 4:
            raise ValueError("pin must be exactly 4 digits")
        return v


# RESPONSE SCHEMAS
class DoesPhoneNumberExistResponse(BaseModel):
    exists: bool


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    phone_number: str
    first_name: str
    last_name: str | None = None


class CreateUserResponse(BaseModel):
    user: UserPublic
