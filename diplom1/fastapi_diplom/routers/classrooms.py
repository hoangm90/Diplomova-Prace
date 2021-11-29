from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import schemas, crud, dependency

router = APIRouter(
    prefix="/classrooms",
    tags=["classrooms"],
)

@router.post("/", response_model=schemas.Classroom)
def create_classroom(classroom: schemas.ItemBase, db: Session = Depends(dependency.get_db)):
    db_classroom = crud.get_item(db, classroom.id, "Classroom")
    if db_classroom:
        raise HTTPException(status_code=400, detail="Classroom already registered")
    
    return crud.create_item(db, classroom, "Classroom")

@router.get("/", response_model=List[schemas.Classroom])
def read_classroom(db: Session = Depends(dependency.get_db)):
    classrooms = crud.get_all_items(db=db, name="Classroom")
    return classrooms

@router.put("/", response_model=schemas.Classroom)
def update_classroom(classroom_id: str, new_classroom: schemas.ItemBase, db: Session = Depends(dependency.get_db)):
    classroom = crud.update_item(db, classroom_id, "Classroom", new_classroom)
    return classroom

@router.delete("/", response_model=schemas.Classroom)
def delete_classroom(classroom_id: str, db:Session = Depends(dependency.get_db)):
    return crud.delete_item(db, classroom_id, "Classroom")