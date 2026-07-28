from datetime import date
from pydantic import BaseModel, ConfigDict

class CardBase(BaseModel):
    member: str
    set_name: str
    condition: str = "mint"
    acquired_on: date | None = None

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    member: str | None = None
    set_name: str | None = None
    condition: str | None = None
    acquired_on: date | None = None

class CardOut(CardBase):
    id: int
    model_config = ConfigDict(from_attributes=True)