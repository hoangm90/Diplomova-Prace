from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import schemas, crud, dependency
import get_data

router = APIRouter(
    prefix="/teachers",
    tags=["teachers"],
)

@router.post("/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.ItemBase, db: Session = Depends(dependency.get_db)):
    db_teacher = crud.get_item(db, teacher.id, "Teacher")
    if db_teacher:
        raise HTTPException(status_code=400, detail="Teacher already registered")
    
    return crud.create_item(db, teacher, "Teacher")

@router.get("/")
def read_teacher():
    teachers = get_data.get_items_with_lessons("Teacher")
    return teachers

@router.put("/", response_model=schemas.Teacher)
def update_teacher(teacher_id: str, new_teacher: schemas.ItemBase, db: Session = Depends(dependency.get_db)):
    teacher = crud.update_item(db, teacher_id, "Teacher", new_teacher)
    return teacher

@router.delete("/", response_model=schemas.Teacher)
def delete_teacher(teacher_id: str, db:Session = Depends(dependency.get_db)):
    return crud.delete_item(db, teacher_id, "Teacher")