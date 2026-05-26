from sqlmodel import SQLModel, create_engine
from sqlmodel import Session

# IMPORTAR MODELOS
from models.client import Client
from models.appointment import Appointment
from models.service import Service
from models.payment import Payment
from models.appointment_service_link import AppointmentServiceLink
from models.user import User


import os

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(
    DATABASE_URL,
    echo=True
)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)