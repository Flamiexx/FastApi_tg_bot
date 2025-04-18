from fastapi import FastAPI
from . import models
from .database import Base, engine
from .routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(router)
Base.metadata.create_all(bind=engine)

