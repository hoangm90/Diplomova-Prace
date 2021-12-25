from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import schemas, crud, dependency
import sort_lessons

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

@router.get("/")
def read_lesson(group_id: str = None, teacher_id: str = None, classroom_id: str = None):
    lessons = sort_lessons.sort_lessons(group_id=group_id, teacher_id=teacher_id, classroom_id=classroom_id)
    return lessons

@router.delete("/all")
def delete_all_lessons(db: Session = Depends(dependency.get_db)):
    return crud.delete_all_lessons(db)

@router.delete("/")
def delete_lesson(lesson_id: str, db: Session = Depends(dependency.get_db)):
    db_lesson = crud.get_lesson(db, lesson_id)
    if db_lesson == None:
        raise HTTPException(status_code=404, detail="Lesson not found!")
    return crud.delete_lesson(db, lesson_id)