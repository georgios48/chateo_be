from pydantic import BaseModel, field_validator

from src.chateo_be.utils.validations import not_empty


class DoesPhoneNumberExistRequest(BaseModel):
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        if not not_empty(v):
            raise ValueError("Phone number cannot be empty")
        return v


class DoesPhoneNumberExistResponse(BaseModel):
    exists: bool
