from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm.session import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    name: str
    email: str
    password: str
    is_verified: bool

class ItemBase(BaseModel):
    title: str
    price: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/item/create")
def create_item(item: ItemBase, db: Session = Depends(get_db)): 
    db_item = models.Item(title = item.title, price = item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)   
    return {"id": db_item.id, "title": db_item.title, "price": db_item.price}    

@app.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item_response = ItemBase(id=item.id, title=item.title, price=item.price)
    return item_response


@app.delete("/item/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    # Retrieve the item from the database based on the provided ID
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Delete the item from the database
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}


@app.put("/item/update/{item_id}")
def update_item(item_id: int, item_update: ItemBase, db: Session = Depends(get_db)):
    # Retrieve the item from the database based on the provided ID
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update the item with the new data
    item.title = item_update.title
    item.price = item_update.price
    db.commit()
    db.refresh(item)
    
    return item