from fastapi import FastAPI
from app.database import get_db, engine, Base
from app.routers import cards, auth


app = FastAPI(title="Photocard Collection API")

Base.metadata.create_all(bind=engine) # quick start

app.include_router(cards.router)
app.include_router(auth.router)
