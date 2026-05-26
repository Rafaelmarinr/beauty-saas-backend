from fastapi import FastAPI
from db.database import create_db_and_tables

from routers import client, appointment, service, payment, report, auth
from models.client import Client
from models.appointment import Appointment
from models.service import Service
from models.user import User

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 🔹 Routers principales
app.include_router(client.router)
app.include_router(appointment.router)
app.include_router(service.router)
app.include_router(payment.router)
app.include_router(report.router)
app.include_router(auth.router)