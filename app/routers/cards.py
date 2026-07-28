from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import CardCreate, CardUpdate, CardOut
from app.auth import get_current_user

router = APIRouter(prefix="/cards", tags=["cards"])

# - Helper -
def _owned_cards(owner_id: int, db: Session):
    return db.query(models.Card).filter(models.Card.owner_id == owner_id)

def _fetch_card(card_id: int, owner_id: int, db: Session) -> models.Card | None:
    return _owned_cards(owner_id=owner_id, db=db).filter(
        models.Card.id == card_id
    ).first()

# - Routes -
@router.get("", response_model=list[CardOut])
def list_cards(member: str | None = None,
               user: models.User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    q = _owned_cards(owner_id= user.id, db=db)
    if member:
        q = q.filter(models.Card.member.ilike(member))
    return q.all()

@router.get("/{card_id}", response_model=CardOut)
def get_card(card_id: int,
             user: models.User = Depends(get_current_user),
             db: Session = Depends(get_db)):
    card = _fetch_card(card_id=card_id, owner_id=user.id, db=db)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.post("", response_model=CardOut,
            status_code=status.HTTP_201_CREATED)
def create_card(payload: CardCreate,
                user: models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    card = models.Card(**payload.model_dump(), owner_id=user.id)
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@router.patch("/{card_id}", response_model=CardOut)
def update_card(card_id: int, payload: CardUpdate,
                user: models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    card = _fetch_card(card_id=card_id, owner_id=user.id, db=db)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(card, field, value)
    db.commit()
    db.refresh(card)
    return card

@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int,
                user: models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    card = _fetch_card(card_id=card_id, owner_id=user.id, db=db)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()