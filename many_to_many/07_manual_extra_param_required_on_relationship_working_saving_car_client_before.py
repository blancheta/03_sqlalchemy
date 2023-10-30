from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Column, DateTime, Boolean

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
    is_rented = Column(Boolean, nullable=False)
    # is_rented <-------- This info needs to be specified manually else SQLAlchemy
    # will have no clue about which value to choose


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
    engine = create_engine("sqlite:///sqlite_07.db")
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        car_1 = Car(model="Tesla Model S")
        car_2 = Car(model="Tesla Model S")

        session.add_all([car_1, car_2])
        session.commit()

        # Client 1 data

        client_1 = Client(
            fullname="John Doe",
        )
        session.add(client_1)
        session.commit()

        # Client 1 rented car_1
        client_1_car_1 = ClientCar(
            client_id=client_1.id,
            car_id=car_1.id,
            is_rented=False
        )

        # Client 2 is currently renting car_2
        client_1_car_2 = ClientCar(
            client_id=client_1.id,
            car_id=car_2.id,
            is_rented=True
        )

        # Client 2 data

        client_2 = Client(
            fullname="Jane Done",
        )
        session.add(client_2)
        session.commit()

        # Client 2 is currently renting car_1
        client_2_car_1 = ClientCar(
            client_id=client_2.id,
            car_id=car_1.id,
            is_rented=True
        )

        # Client 2 rented car_2 in the past
        client_2_car_2 = ClientCar(
            client_id=client_2.id,
            car_id=car_2.id,
            is_rented=False
        )

        session.add_all([
            client_1_car_1,
            client_1_car_2,
            client_2_car_1,
            client_2_car_2
        ])
        session.commit()

