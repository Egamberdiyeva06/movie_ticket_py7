from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select

from schemas import TicketCreate, TicketOut, UserBase, UserCreate, UserOut
from database import Base, get_db, engine
from models import Ticket, User


Base.metadata.create_all(bind=engine)
user_router = APIRouter(prefix='/api/users', tags=["Users"])
ticket_router = APIRouter(prefix='/api/tickets', tags=["Tickets"])


@user_router.get('/', response_model=list[UserOut])
def get_users(db=Depends(get_db)):
    stmt = select(User)
    users = db.scalars(stmt).all()
    return users


@user_router.post('/', response_model=UserOut)
def create_user(user_in: UserCreate, db=Depends(get_db)):
    existing_user = db.scalar(select(User).where(User.first_name == user_in.first_name,
                                                 User.last_name == user_in.last_name, 
                                                 User.password == user_in.password))
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu foydalanuvchi nomi band.")
    
    new_user = User(**user_in.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@user_router.get('/me', response_model=UserOut)
def get_user_me(user_id: int, db=Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return user


@user_router.put('/me', response_model=UserOut)
def update_user_me(user_id: int, user_update: UserBase, db=Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    
    user.first_name = user_update.first_name
    user.last_name = user_update.last_name

    db.commit()
    db.refresh(user)
    return user



@ticket_router.post('/', response_model=TicketOut)
def create_ticket(ticket_in: TicketCreate, user_id: int, db = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.movie_name == ticket_in.movie_name,
                                Ticket.seat_number == ticket_in.seat_number)
    existing_ticket = db.scalar(stmt)
    if existing_ticket:
        raise HTTPException(status_code=404, detail="Bu bilet allaqachon sotilgan.")
    
                
    price = 80000 if ticket_in.is_vip else 40000

    ticket =Ticket(
        **ticket_in.model_dump(),
        price = price, 
        user_id = user_id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@ticket_router.get('/', response_model=list[TicketOut])
def get_tickets(db = Depends(get_db)):
    stmt = select(Ticket)
    tickets = db.scalars(stmt).all()

    return tickets


@ticket_router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket_by_id(ticket_id: int, db = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.id == ticket_id)
    ticket = db.scalar(stmt)
    if not ticket:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return ticket



@ticket_router.put("/{ticket_id}", response_model=TicketOut)
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


@ticket_router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db=Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Chipta topilmadi!")

    db.delete(ticket)
    db.commit()

    return {"message": "Chipta o'chirildi!"}