from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from schemas import TicketCreate, TicketOut, TicketGet
from database import Base, get_db, engine
from models import Ticket


Base.metadata.create_all(bind=engine)
api_router = APIRouter(prefix='/api/tickets')



@api_router.post('/', response_model=TicketOut)
def create_ticket(ticket_in: TicketCreate, db = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.movie_name == ticket_in.movie_name,
                                Ticket.seat_number == ticket_in.seat_number)
    existing_ticket = db.scalar(stmt)
    if existing_ticket:
        raise HTTPException(status_code=404, detail="Bu bilet allaqachon sotilgan.")
    
                
    price = 80000 if ticket_in.is_vip else 40000

    ticket =Ticket(
        **ticket_in.model_dump(),
        price = price
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket

@api_router.get('/', response_model=list[TicketOut])
def get_tickets(db = Depends(get_db)):
    stmt = select(Ticket)
    tickets = db.scalars(stmt).all()

    return tickets

@api_router.get("/{ticket_id}", response_model=TicketGet)
def get_ticket_by_id(ticket_id: int, db = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.id == ticket_id)
    ticket = db.scalar(stmt)
    if not ticket:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return ticket



@api_router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, ticket_in: TicketCreate, db=Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Chipta topilmadi!")

    ticket.movie_name = ticket_in.movie_name
    ticket.customer_name = ticket_in.customer_name
    ticket.seat_number = ticket_in.seat_number
    ticket.is_vip = ticket_in.is_vip

    db.commit()
    db.refresh(ticket)

    return ticket

@api_router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db=Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Chipta topilmadi!")

    db.delete(ticket)
    db.commit()

    return {"message": "Chipta o'chirildi!"}