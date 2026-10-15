
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
) -> Ticket:
    """Create and persist a customer support ticket."""
    ticket = Ticket(**payload.model_dump())

    try:
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Failed to create ticket")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create ticket",
        )

    logger.info("Ticket created: id=%s", ticket.id)
    return ticket



@router.get(
    "",
    response_model=list[TicketResponse],
    status_code=status.HTTP_200_OK,
)
def list_tickets(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
) -> list[Ticket]:
    """Retrieve tickets with pagination."""

    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid pagination parameters",
        )

    statement = (
        select(Ticket)
        .order_by(Ticket.id.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Ticket not found"},
    },
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
) -> Ticket:
    """Retrieve a ticket by its ID."""

    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


@router.patch(
    "/{ticket_id}",
    response_model=TicketResponse,
    responses={404: {"description": "Ticket not found"}},
)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    db: Session = Depends(get_db),
) -> Ticket:
    """Partially update an existing ticket."""

    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    updates = payload.model_dump(exclude_unset=True)

    if any(value is None for value in updates.values()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ticket fields cannot be null",
        )

    for field, value in updates.items():
        setattr(ticket, field, value)

    try:
        db.commit()
        db.refresh(ticket)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Failed to update ticket id=%s", ticket_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update ticket",
        )

    logger.info("Ticket updated: id=%s", ticket_id)
    return ticket


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Ticket not found"}},
)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Permanently delete a ticket by ID."""

    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    try:
        db.delete(ticket)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Failed to delete ticket id=%s", ticket_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete ticket",
        )

    logger.info("Ticket deleted: id=%s", ticket_id)
