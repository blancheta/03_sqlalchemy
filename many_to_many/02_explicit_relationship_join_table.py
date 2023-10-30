from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
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
    engine = create_engine("sqlite:///sqlite_02.db")
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        car_1 = Car(model="Tesla Model S")
        car_2 = Car(model="Ferrari 458")

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

        client_1 = session.query(Client).filter_by(
            fullname="John Doe"
        ).first()

        print("Car rentals for client 1: ", client_1.car_rentals)

        client_2 = session.query(Client).filter_by(
            fullname="Jane Done"
        ).first()

        print("Car rentals for client 2: ", client_2.car_rentals)

        car_1 = session.query(Car).filter_by(
            model="Tesla Model S"
        ).first()

        print("Clients who rented car_1: ", car_1.clients)

        car_2 = session.query(Car).filter_by(
            model="Ferrari 458"
        ).first()

        print("Clients who rented car_2: ", car_2.clients)

        print("!!!! HERE a client can rent multiple cars \n"
              "and a car can be rented by multiple clients. \n"
              "No information is lost")
