
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

def test_update_ticket_database_failure(
    client: TestClient,
    db_session: Session,
) -> None:
    """A failed update commit returns 500 and triggers rollback."""

    created = client.post(
        "/tickets",
        json={
            "subject": "Original subject",
            "description": "Testing PATCH transaction rollback",
        },
    )

    assert created.status_code == 201
    ticket_id = created.json()["id"]

    with (
        patch.object(
            db_session,
            "commit",
            side_effect=SQLAlchemyError("Simulated database failure"),
        ) as mock_commit,
        patch.object(
            db_session,
            "rollback",
            wraps=db_session.rollback,
        ) as mock_rollback,
    ):
        response = client.patch(
            f"/tickets/{ticket_id}",
            json={"subject": "Updated subject"},
        )

        assert response.status_code == 500
        assert response.json() == {
            "detail": "Unable to update ticket"
        }

        mock_commit.assert_called_once()
        mock_rollback.assert_called_once()


def test_create_ticket_success(client: TestClient) -> None:
    """A valid ticket should return HTTP 201."""
    payload = {
        "subject": "Login issue",
        "description": "Customer cannot log in.",
        "priority": "high",
    }

    response = client.post("/tickets", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["subject"] == payload["subject"]
    assert data["description"] == payload["description"]
    assert data["priority"] == "high"
    assert data["status"] == "open"
    assert data["created_at"]
    assert data["updated_at"]


def test_create_ticket_invalid_subject(
    client: TestClient,
) -> None:
    """An empty subject should return HTTP 422."""
    payload = {
        "subject": "",
        "description": "Customer cannot log in.",
        "priority": "high",
    }

    response = client.post("/tickets", json=payload)

    assert response.status_code == 422


def test_create_ticket_persistence(
    client: TestClient,
    db_session: Session,
) -> None:
    """A created ticket should be visible in PostgreSQL."""
    payload = {
        "subject": "Payment failure",
        "description": "Payment was declined.",
        "priority": "urgent",
    }

    response = client.post("/tickets", json=payload)

    assert response.status_code == 201

    ticket_id = response.json()["id"]

    ticket = db_session.scalar(
        select(Ticket).where(Ticket.id == ticket_id)
    )

    assert ticket is not None
    assert ticket.subject == "Payment failure"
    assert ticket.priority == "urgent"


def test_list_tickets_success(client: TestClient) -> None:
    """Created tickets should appear in the ticket list."""
    client.post(
        "/tickets",
        json={
            "subject": "Login issue",
            "description": "Unable to log in",
            "priority": "high",
        },
    )

    response = client.get("/tickets?skip=0&limit=20")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["subject"] == "Login issue"


def test_list_tickets_pagination(client: TestClient) -> None:
    """Pagination should skip the requested number of tickets."""
    for i in range(3):
        response = client.post(
            "/tickets",
            json={
                "subject": f"Ticket {i}",
                "description": "Test description",
                "priority": "medium",
            },
        )
        assert response.status_code == 201

    response = client.get("/tickets?skip=1&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["subject"] == "Ticket 1"


def test_list_tickets_invalid_pagination(
    client: TestClient,
) -> None:
    """Invalid pagination values should return HTTP 422."""
    response = client.get("/tickets?skip=-1&limit=20")

    assert response.status_code == 422

    response = client.get("/tickets?skip=0&limit=101")

    assert response.status_code == 422


def test_get_ticket_success(client: TestClient) -> None:
    """Retrieve an existing ticket by ID."""
    create_response = client.post(
        "/tickets",
        json={
            "subject": "Password reset",
            "description": "Customer forgot password",
            "priority": "medium",
        },
    )

    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]

    response = client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 200
    assert response.json()["id"] == ticket_id
    assert response.json()["subject"] == "Password reset"


def test_get_ticket_not_found(client: TestClient) -> None:
    """Return HTTP 404 when a ticket does not exist."""
    response = client.get("/tickets/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ticket not found"
    }


def test_update_ticket_success(client: TestClient) -> None:
    """Updating status must preserve other ticket fields."""
    created = client.post(
        "/tickets",
        json={
            "subject": "Login issue",
            "description": "Cannot log in",
            "priority": "high",
        },
    )
    assert created.status_code == 201

    ticket_id = created.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={"status": "resolved"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "resolved"
    assert data["subject"] == "Login issue"
    assert data["description"] == "Cannot log in"
    assert data["priority"] == "high"


def test_update_ticket_invalid_status(client: TestClient) -> None:
    """Unsupported status values must return HTTP 422."""
    created = client.post(
        "/tickets",
        json={
            "subject": "Payment issue",
            "description": "Payment failed",
        },
    )
    assert created.status_code == 201

    ticket_id = created.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={"status": "invalid_status"},
    )

    assert response.status_code == 422


def test_update_ticket_not_found(client: TestClient) -> None:
    """Updating a nonexistent ticket must return HTTP 404."""
    response = client.patch(
        "/tickets/999999",
        json={"status": "resolved"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_update_ticket_rejects_null(client: TestClient) -> None:
    """Explicit null values must be rejected."""
    created = client.post(
        "/tickets",
        json={
            "subject": "Account issue",
            "description": "Account locked",
        },
    )
    assert created.status_code == 201

    ticket_id = created.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={"subject": None},
    )

    assert response.status_code == 422


def test_delete_ticket_success(client: TestClient) -> None:
    """Deleting a ticket removes it from the database."""
    created = client.post(
        "/tickets",
        json={
            "subject": "Temporary ticket",
            "description": "Ticket created for deletion testing",
        },
    )
    assert created.status_code == 201
    ticket_id = created.json()["id"]

    response = client.delete(f"/tickets/{ticket_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/tickets/{ticket_id}")

    assert get_response.status_code == 404


def test_delete_ticket_not_found(client: TestClient) -> None:
    """Deleting a nonexistent ticket returns HTTP 404."""
    response = client.delete("/tickets/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ticket not found"
    }

def test_delete_ticket_database_failure(
    client: TestClient,
    db_session: Session,
) -> None:
    """Database commit failure returns 500 and triggers rollback."""

    created = client.post(
        "/tickets",
        json={
            "subject": "Rollback test",
            "description": "Verify failed deletion handling",
        },
    )

    assert created.status_code == 201
    ticket_id = created.json()["id"]

    with (
        patch.object(
            db_session,
            "commit",
            side_effect=SQLAlchemyError("Simulated database failure"),
        ) as mock_commit,
        patch.object(
            db_session,
            "rollback",
            wraps=db_session.rollback,
        ) as mock_rollback,
    ):
        response = client.delete(f"/tickets/{ticket_id}")

        assert response.status_code == 500
        assert response.json() == {
            "detail": "Unable to delete ticket"
        }

        mock_commit.assert_called_once()
        mock_rollback.assert_called_once()

def test_create_ticket_database_failure(
    client: TestClient,
    db_session: Session,
) -> None:
    """A failed database commit returns 500 and triggers rollback."""

    with (
        patch.object(
            db_session,
            "commit",
            side_effect=SQLAlchemyError("Simulated database failure"),
        ) as mock_commit,
        patch.object(
            db_session,
            "rollback",
            wraps=db_session.rollback,
        ) as mock_rollback,
    ):
        response = client.post(
            "/tickets",
            json={
                "subject": "Database failure test",
                "description": "Testing POST transaction rollback",
            },
        )

        assert response.status_code == 500
        assert response.json() == {
            "detail": "Unable to create ticket"
        }

        mock_commit.assert_called_once()
        mock_rollback.assert_called_once()