from pydantic import BaseModel, Field
from typing import Literal


class UserBase(BaseModel):
    first_name: str = Field(max_length=200)
    last_name: str = Field(max_length=200)
    role: Literal["admin", 'user'] = 'user'


class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=50)


class UserOut(UserBase):
    id: int
    tickets: list["TicketOut"] = []

    class Config: 
        from_attributes = True


class TicketBase(BaseModel):
    movie_name: str = Field(max_length=200)
    customer_name: str = Field(max_length=100)
    seat_number: int = Field(ge=1, le=50)
    is_vip: bool = False


class TicketCreate(TicketBase):
    pass


class TicketOut(TicketBase):
    id: int = Field(ge=1)
    price: float = Field(default=0)
    user_id: int

    class Config:
        from_attributes = True