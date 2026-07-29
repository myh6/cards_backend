from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, cards

app = FastAPI(title="Photocard Collection API")

Base.metadata.create_all(bind=engine) # quick start

app.include_router(cards.router)
app.include_router(auth.router)
