from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import models_and_schemas.schemas as schemas
import crud
import manage_database.dependency as dependency
import helper_function.get_data as get_data

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
)

@router.post("/", response_model=schemas.Group)
def create_group(group: schemas.ItemBase, db: Session = Depends(dependency.get_db)):
    db_group = crud.get_item(db, group.id, "Group")
    if db_group:
        raise HTTPException(status_code=400, detail="Group already registered")
    
    return crud.create_item(db, group, "Group")

@router.get("/")
def read_group():
    groups = get_data.get_items_with_lessons("Group")
    return groups

@router.put("/", response_model=schemas.Group)
def update_group(group_id: str, new_group: schemas.ItemBase, db: Session = Depends(dependency.get_db)):
    group = crud.update_item(db, group_id, "Group", new_group)
    return group

@router.delete("/", response_model=schemas.Group)
def delete_group(group_id: str, db:Session = Depends(dependency.get_db)):
    return crud.delete_item(db, group_id, "Group")