
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


TicketStatus = Literal["open", "in_progress", "resolved", "closed"]
TicketPriority = Literal["low", "medium", "high", "urgent"]

def validate_non_blank(value: str) -> str:
    if not value.strip():
        raise ValueError("Field cannot be blank")
    return value.strip()

class TicketCreate(BaseModel):
    subject: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    priority: TicketPriority = "medium"
    @field_validator("subject", "description")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return validate_non_blank(value)


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: datetime


class TicketUpdate(BaseModel):
    subject: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        min_length=1,
    )
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    @field_validator("subject", "description")
    @classmethod
    def validate_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return validate_non_blank(value)

