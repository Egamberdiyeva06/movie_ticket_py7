from fastapi import APIRouter, HTTPException

from schemas import TicketCreate, TicketOut, TicketGet

api_router = APIRouter(prefix='/api/tickets')

tickets = []
current_ticket_id = 1

@api_router.post('/', response_model=TicketOut)
def create_ticket(ticket_in: TicketCreate):
    global current_ticket_id

    for sold_ticket in tickets:
        if (sold_ticket["seat_number"] == ticket_in.seat_number and
            sold_ticket["movie_name"] == ticket_in.movie_name):
            raise HTTPException(status_code=404, detail="Bu bilet allaqachon sotilgan.")
                
    price = 80000 if ticket_in.is_vip else 40000

    new_ticket = {
        "ticket_id" : current_ticket_id,
        "customer_name" : ticket_in.customer_name,
        "seat_number" : ticket_in.seat_number,
        "movie_name" : ticket_in.movie_name,
        "is_vip": ticket_in.is_vip,
        "price": price
    }
    tickets.append(new_ticket)
    current_ticket_id += 1

    return new_ticket

@api_router.get('/', response_model=list[TicketGet])
def get_ticket():
    return tickets

@api_router.get("/{ticket_id}", response_model=TicketGet)
def get_ticket_by_id(ticket_id: int):
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Topilmadi")

@api_router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, ticket_in: TicketCreate):
    for i in tickets:
        if i["ticket_id"] == ticket_id:
            i["customer_name"] = ticket_in.customer_name
            i["seat_number"] = ticket_in.seat_number
            i["movie_name"] = ticket_in.movie_name
            i["is_vip"] = ticket_in.is_vip

            i["price"] = 80000 if ticket_in.is_vip else 40000

            return i
        
    raise HTTPException(status_code=404, detail="Chipta topilmadi!")


@api_router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int):
    for i, j in enumerate(tickets):
        if j["ticket_id"] == ticket_id:
            tickets.pop(i)
            return {"massage" : "Chipta o'chirildi!"}
        
    raise HTTPException(status_code=404, detail="Chipta topilmadi!")