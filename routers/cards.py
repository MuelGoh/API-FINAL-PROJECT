from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Cards
from database import get_db
from .auth import get_current_user

router = APIRouter()


class Card(BaseModel):
    id: int | None = None
    name: str = Field(min_length=1)
    type: str = Field(min_length=1)
    elixir: str = Field(min_length=1)
    default_level: str = Field(min_length=1)
    use_rate: str = Field(min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "undying hunter",
                "type": "epic",
                "elixir": "4",
                "default_level": "9",
                "use_rate": "68%"
            }
        }


@router.get("", status_code=status.HTTP_200_OK)
async def get_card_registry(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user:
        return db.query(Cards).all()
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_card(card_data: Card, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_task = Cards(**card_data.model_dump())

    db.add(new_task)
    db.commit()


@router.get("/{card_id}", status_code=status.HTTP_200_OK)
async def get_card_by_id(card_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user:
        card = db.query(Cards).filter(card_id == Cards.id).first()
        if card is not None:
            return card

        raise HTTPException(status_code=404, detail=f"Card with id#{card_id} not found")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


@router.put("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_card_by_id(card_id: int, card_data: Card, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    card = db.query(Cards).filter(card_id == Cards.id).first()

    if card is None:
        raise HTTPException(status_code=404, detail=f"Card with id#{card_id} not found")

    card.name = card_data.name
    card.type = card_data.type
    card.elixir = card_data.elixir
    card.default_level = card_data.default_level
    card.use_rate = card_data.use_rate

    db.add(card)
    db.commit()


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card_by_id(card_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    delete_card = db.query(Cards).filter(Cards.id == card_id).first()

    if delete_card is None:
        raise HTTPException(status_code=404, detail=f"Card with id#{card_id} not found")

    db.query(Cards).filter(Cards.id == card_id).delete()
    db.commit()