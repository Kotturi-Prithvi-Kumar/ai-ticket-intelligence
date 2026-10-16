import pytest
from pydantic import ValidationError

from app.schemas.ticket import TicketCreate, TicketUpdate


@pytest.mark.parametrize(
    "subject",
    ["", " ", "   ", "\t", "\n"],
)
def test_reject_blank_subject(subject: str) -> None:
    with pytest.raises(ValidationError):
        TicketCreate(
            subject=subject,
            description="Valid description",
        )


@pytest.mark.parametrize(
    "description",
    ["", " ", "   ", "\t", "\n"],
)
def test_reject_blank_description(description: str) -> None:
    with pytest.raises(ValidationError):
        TicketCreate(
            subject="Valid subject",
            description=description,
        )


@pytest.mark.parametrize(
    "priority",
    ["critical", "invalid", "HIGH", ""],
)
def test_reject_invalid_priority(priority: str) -> None:
    with pytest.raises(ValidationError):
        TicketCreate(
            subject="Valid subject",
            description="Valid description",
            priority=priority,
        )


def test_strip_whitespace() -> None:
    ticket = TicketCreate(
        subject="  Login issue  ",
        description="  Cannot log in  ",
    )

    assert ticket.subject == "Login issue"
    assert ticket.description == "Cannot log in"


def test_reject_invalid_status_update() -> None:
    with pytest.raises(ValidationError):
        TicketUpdate(status="invalid")


def test_reject_blank_subject_update() -> None:
    with pytest.raises(ValidationError):
        TicketUpdate(subject="   ")