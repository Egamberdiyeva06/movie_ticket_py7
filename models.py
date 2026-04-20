from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey


from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=30))
    last_name: Mapped[str] = mapped_column(String(length=30))
    password: Mapped[str] = mapped_column(String(length=50))
    
    role: Mapped[str] = mapped_column(String(10), default="user")

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")


class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_name: Mapped[str] = mapped_column(String(length=100))
    customer_name: Mapped[str] = mapped_column(String(length=100))
    seat_number: Mapped[int] = mapped_column(Integer)
    is_vip: Mapped[bool] = mapped_column(Boolean, default=False)
    price: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates='tickets')