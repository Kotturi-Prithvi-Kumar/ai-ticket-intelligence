import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.ticket import Ticket


@pytest.mark.parametrize(
    "payload",
    [
        {
            "subject": "   ",
            "description": "Valid description",
        },
        {
            "subject": "Valid subject",

            "description": "   ",
        },
        {
            "subject": "Valid subject",
            "description": "Valid description",
            "priority": "critical",
        },
        {
            "subject": "A" * 256,
            "description": "Valid description",
        },
    ],
)
def test_create_ticket_invalid_payload(
    client: TestClient,
    payload: dict,
) -> None:
    """Invalid ticket payloads must return HTTP 422."""
    response = client.post("/tickets", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_create_ticket_trims_whitespace(
    client: TestClient,
) -> None:
    """Valid text should be normalized before persistence."""
    response = client.post(
        "/tickets",
        json={
            "subject": "  Login issue  ",
            "description": "  Cannot log in  ",
        },
    )

    assert response.status_code == 201
    assert response.json()["subject"] == "Login issue"
    assert response.json()["description"] == "Cannot log in"


@pytest.mark.parametrize(
    "update_payload",
    [
        {"subject": "   "},
        {"description": "   "},
        {"priority": "critical"},
        {"status": "unknown"},
    ],
)
def test_invalid_patch_preserves_ticket(
    client: TestClient,
    db_session: Session,
    update_payload: dict,
) -> None:
    """Rejected updates must not modify persisted ticket data."""
    created = client.post(
        "/tickets",
        json={
            "subject": "Original subject",
            "description": "Original description",
            "priority": "medium",
        },
    )

    assert created.status_code == 201
    ticket_id = created.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json=update_payload,
    )

    assert response.status_code == 422

    db_session.expire_all()

    ticket = db_session.scalar(
        select(Ticket).where(Ticket.id == ticket_id)
    )

    assert ticket is not None
    assert ticket.subject == "Original subject"
    assert ticket.description == "Original description"
    assert ticket.priority == "medium"
    assert ticket.status == "open"