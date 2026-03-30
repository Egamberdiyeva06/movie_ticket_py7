from pydantic import BaseModel, Field

class TicketCreate(BaseModel):
    movie_name: str = Field(max_length=200)
    seat_number: int = Field(ge=1, le=50)
    customer_name: str = Field(max_length=100)
    is_vip: bool = False


class TicketOut(BaseModel):
    id: int = Field(ge=1)
    movie_name: str = Field(max_length=200)
    seat_number: int = Field(ge=1, le=50)
    customer_name: str = Field(max_length=100)
    is_vip: bool = False
    price: float = Field(default=0)

    class Config:
        from_attributes = True

class TicketGet(BaseModel):
    id: int
    movie_name: str
    seat_number: int
    customer_name: str
    is_vip: bool
    price: float

    class Config:
        from_attributes = True