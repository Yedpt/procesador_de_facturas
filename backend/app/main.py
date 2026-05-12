from fastapi import FastAPI
from app.controllers.health import router as health_router
from app.controllers.invoices import router as invoices_router
from app.config.database import Base, engine
from app.models import entities # noqa: F401

app = FastAPI(title="Procesador de Facturas")

Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(invoices_router)