from fastapi import FastAPI
from app.controllers.health import router as health_router
from app.controllers.invoices import router as invoices_router

app = FastAPI(title="Procesador de Facturas")

app.include_router(health_router)
app.include_router(invoices_router)