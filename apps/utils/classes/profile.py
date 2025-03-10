from typing import Optional

from pydantic import BaseModel, Field, field_validator

DEFAULT_BOXROOM_NUMBER = 75080


class ForumProfile(BaseModel):
    creatures: str = Field(default_factory=str, alias="customFields[35]")
    objects: str = Field(default_factory=str, alias="customFields[36]")
    galleons: int = Field(default_factory=int, alias="customFields[12]")
    level: int = Field(default_factory=int, alias="customFields[43]")
    character: int = Field(default_factory=int, alias="customFields[65]")
    boxroom_number: int = Field(DEFAULT_BOXROOM_NUMBER, alias="customFields[66]")
    avatar: Optional[str] = Field(None)
    vault: int = Field(..., alias="customFields[64]")
    formatted_name: str = Field(...)
    nick: str = Field(...)

    @field_validator("avatar", mode="before")
    @classmethod
    def enforce_max_length(cls, value):
        if value and len(value) <= 512:
            return value

        return None

    @field_validator("galleons", "level", "character", mode="before")
    @classmethod
    def convert_empty_to_zero(cls, value):
        if value == "" or value is None:
            return 0

        return int(value)

    @field_validator("boxroom_number", mode="before")
    @classmethod
    def convert_empty_to_default(cls, value):
        if value == "" or value is None:
            return DEFAULT_BOXROOM_NUMBER

        return int(value)

    class Config:
        populate_by_name = True
