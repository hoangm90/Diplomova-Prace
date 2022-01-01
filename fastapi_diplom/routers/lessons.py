from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import models_and_schemas.schemas as schemas 
import crud
import manage_database.dependency as dependency
import helper_function.sort_lessons as sort_lessons

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

@router.put("/")
def update_lesson(
    updated_lesson: schemas.Create_lesson,
    db: Session = Depends(dependency.get_db)
    ):
    db_lesson = crud.get_lesson(db, updated_lesson.lesson.lesson_id)
    if db_lesson == None:
        raise HTTPException(status_code=404, detail="Lesson not found!")
    return crud.update_lesson(db, updated_lesson.lesson, updated_lesson.group_ids, updated_lesson.teacher_ids, updated_lesson.classroom_ids)

@router.put("/change_time")
def change_lesson_time(lesson_id: str, new_time: str, db: Session = Depends(dependency.get_db)):
    db_lesson = crud.get_lesson(db, lesson_id)
    if db_lesson == None:
        raise HTTPException(status_code=404, detail="Lesson not found!")
    return crud.change_lesson_time(db, lesson_id, new_time)