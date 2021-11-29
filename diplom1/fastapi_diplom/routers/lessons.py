from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import schemas, crud, dependency

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"],
)

@router.post("/", response_model=schemas.Lesson)
def create_lesson(
    created_lesson: schemas.Create_lesson,
    db: Session = Depends(dependency.get_db)
    ):
    db_lesson = crud.get_lesson(db, created_lesson.lesson.lesson_id)
    if db_lesson:
        raise HTTPException(status_code=400, detail="Lesson already registered")

    return crud.create_lesson(db, created_lesson.lesson, created_lesson.group_ids, created_lesson.teacher_ids, created_lesson.classroom_ids)

@router.get("/", response_model=List[schemas.Lesson])
def read_lesson(db: Session = Depends(dependency.get_db)):
    lessons = crud.get_all_lessons(db=db)
    return lessons