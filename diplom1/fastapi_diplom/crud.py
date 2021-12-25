from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
import models, schemas

# function for lessons
def get_all_lessons(db: Session):
    return db.query(models.Lesson).all()

def get_lesson(db: Session, lesson_id: str):
    return db.query(models.Lesson).filter(models.Lesson.lesson_id == lesson_id).first()

def create_lesson(
    db: Session, 
    lesson: schemas.LessonBase, 
    group_ids: List[str],
    teacher_ids: List[str],
    classroom_ids: List[str]
    ):
    db_lesson = models.Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)

    for group_id in group_ids:
        db_relation_lesson_group = models.Relation_lesson_group(lesson_id=lesson.lesson_id, group_id=group_id)
        db.add(db_relation_lesson_group)
        db.commit()
        db.refresh(db_relation_lesson_group)
    
    for teacher_id in teacher_ids:
        db_relation_lesson_teacher = models.Relation_lesson_teacher(lesson_id=lesson.lesson_id, teacher_id=teacher_id)
        db.add(db_relation_lesson_teacher)
        db.commit()
        db.refresh(db_relation_lesson_teacher)
    
    for classroom_id in classroom_ids:
        db_relation_lesson_classroom = models.Relation_lesson_classroom(lesson_id=lesson.lesson_id, classroom_id=classroom_id)
        db.add(db_relation_lesson_classroom)
        db.commit()
        db.refresh(db_relation_lesson_classroom)

    return db_lesson

###############################################################
# functions for groups, teachers, classrooms
def get_all_items(db: Session, name: str):
    item_model = getattr(models, name)
    return db.query(item_model).all()

def get_item(db: Session, id: str, name: str):
    item_model = getattr(models, name)
    item_id = getattr(item_model, name.lower() + "_id")
    return db.query(item_model).filter(item_id == id).first()

def update_item(db: Session, id: str, name: str, new_item: schemas.ItemBase):
    item_model = getattr(models, name)
    item_id = getattr(item_model, name.lower() + "_id")
    db_item = db.query(item_model).filter(item_id == id).first()
    db_item_id = name.lower() + "_id"  # group_id or teacher_id or classroom_id
    if db_item:
        if new_item.id != id:
            if db.query(item_model).filter(item_id == new_item.id).first():
                raise HTTPException(status_code=400, detail="The " + name.lower() + " Id has been used by another")
            setattr(db_item, db_item_id, new_item.id)
            rela_model = getattr(models, "Relation_lesson_" + name.lower())
            rela_model_id = getattr(rela_model, db_item_id)
            list_db_rela = db.query(rela_model).filter(rela_model_id == id).all()
            for db_re in list_db_rela:
                setattr(db_re, db_item_id, new_item.id)
        
        db_item_name = name.lower() + "_name"  # group_name or teacher_name or classroom_name
        setattr(db_item, db_item_name, new_item.name)
        db.commit()
        db.refresh(db_item)
        return db_item
    raise HTTPException(status_code=404, detail= name + " not found")
    
def create_item(db:Session, item: schemas.ItemBase, name: str):
    item_model = getattr(models, name)
    db_item = item_model()
    setattr(db_item, name.lower()+"_id", item.id)
    setattr(db_item, name.lower()+"_name", item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

def delete_item(db: Session, id: str, name: str):
    item_model = getattr(models, name)
    item_id = getattr(item_model, name.lower() + "_id")
    db_item = db.query(item_model).filter(item_id == id).first()
    db_item_id = name.lower() + "_id"  # group_id or teacher_id or classroom_id
    if db_item:
        rela_model = getattr(models, "Relation_lesson_" + name.lower())
        rela_model_id = getattr(rela_model, db_item_id)
        list_db_rela = db.query(rela_model).filter(rela_model_id == id).all()
        for db_re in list_db_rela:
            db.delete(db_re)
        db.delete(db_item)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail= name + " not found")
    return db_item
