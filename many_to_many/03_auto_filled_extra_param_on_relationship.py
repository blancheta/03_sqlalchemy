from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Column, DateTime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass


class ClientCar(Base):
    __tablename__ = "client_car"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    rented_time = Column(DateTime, default=datetime.utcnow)


class Client(Base):
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[Optional[str]]
    car_rentals: Mapped[List["Car"]] = relationship(
        secondary=ClientCar.__tablename__,
        back_populates="clients",
    )

    def __repr__(self) -> str:
        return f"Client(id={self.id!r}, fullname={self.fullname!r})"


class Car(Base):
    __tablename__ = "car"
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str]

    clients: Mapped[List["Client"]] = relationship(
        secondary=ClientCar.__tablename__,
        back_populates="car_rentals"
    )

    def __repr__(self) -> str:
        return f"Car(id={self.id!r}, model={self.model!r})"


if __name__ == "__main__":
    engine = create_engine("sqlite:///sqlite_03.db")
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        car_1 = Car(model="Tesla Model S")
        car_2 = Car(model="Tesla Model S")

        client_1 = Client(
            fullname="John Doe",
            car_rentals=[
                car_1,
                car_2
            ]
        )

        client_2 = Client(
            fullname="Jane Done",
            car_rentals=[
                car_1,
                car_2
            ]
        )

        session.add_all([client_1, client_2])
        session.commit()

        print(
            "!!!! HERE we are added automatically"
            "the creation date \n"
            "to keep track of when a car has been rented by who"
        )