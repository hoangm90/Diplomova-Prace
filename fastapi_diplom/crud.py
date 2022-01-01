from sqlalchemy.orm import Session
from typing import List

from fastapi import HTTPException
from models_and_schemas import models, schemas
import helper_function.color_to_time as color_to_time

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

def update_lesson(
    db: Session, 
    lesson: schemas.LessonBase, 
    group_ids: List[str],
    teacher_ids: List[str],
    classroom_ids: List[str]
    ):
    can_change = True
    dict_te = {}
    dict_gr = {}

    for u in db.query(models.Relation_lesson_teacher).all():
        if dict_te.get(u.__dict__["lesson_id"]) == None:
            dict_te[u.__dict__["lesson_id"]] = []
        dict_te[u.__dict__["lesson_id"]].append(u.__dict__["teacher_id"])
    
    for u in db.query(models.Relation_lesson_group).all():
        if dict_gr.get(u.__dict__["lesson_id"]) == None:
            dict_gr[u.__dict__["lesson_id"]] = []
        dict_gr[u.__dict__["lesson_id"]].append(u.__dict__["group_id"])
    
    dict_les_te = {}
    dict_les_gr = {}
    for te in teacher_ids:
        dict_les_te[te] = True
    for gr in group_ids:
        dict_les_gr[gr] = True

    for ls in db.query(models.Lesson).filter(models.Lesson.color == lesson.color).all():
        if ls.__dict__["chosen_classroom"] != "" and ls.__dict__["chosen_classroom"] == lesson.chosen_classroom:
            can_change = False
            break
        if dict_te.get(ls.__dict__["lesson_id"]) != None:
            for te in dict_te.get(ls.__dict__["lesson_id"]):
                if dict_les_te.get(te):
                    can_change = False
                    break
        if not can_change:
            break
        
        if dict_gr.get(ls.__dict__["lesson_id"]):
            for gr in dict_gr.get(ls.__dict__["lesson_id"]):
                if dict_les_gr.get(gr):
                    can_change = False
                    break
        if not can_change:
            break
    
    if can_change:
        delete_lesson(db, lesson.lesson_id)
        create_lesson(db, lesson, group_ids, teacher_ids, classroom_ids)
    else:
        raise HTTPException(status_code=400, detail="The lesson cannot be added to this time!")
    return 
        
def change_lesson_time(db: Session, lesson_id: str, new_time: str):
    color = color_to_time.time_to_color(new_time)
    if color == -1:
        raise HTTPException(status_code=400, detail="The time format is wrong!")

    dict_te = {}
    dict_gr = {}  
    for u in db.query(models.Relation_lesson_teacher).all():
        if dict_te.get(u.__dict__["lesson_id"]) == None:
            dict_te[u.__dict__["lesson_id"]] = []
        dict_te[u.__dict__["lesson_id"]].append(u.__dict__["teacher_id"])
    
    for u in db.query(models.Relation_lesson_group).all():
        if dict_gr.get(u.__dict__["lesson_id"]) == None:
            dict_gr[u.__dict__["lesson_id"]] = []
        dict_gr[u.__dict__["lesson_id"]].append(u.__dict__["group_id"])
    
    dict_les_te = {}
    dict_les_gr = {}
    for db_rela in db.query(models.Relation_lesson_teacher).filter(models.Relation_lesson_teacher.lesson_id == lesson_id).all():
        dict_les_te[db_rela.teacher_id] = True
    for db_rela in db.query(models.Relation_lesson_group).filter(models.Relation_lesson_group.lesson_id == lesson_id).all():
        dict_les_gr[db_rela.group_id] = True
    chosen_cl = db.query(models.Lesson).filter(models.Lesson.lesson_id == lesson_id).first().chosen_classroom
    
    can_change = True
    for db_lesson in db.query(models.Lesson).filter(models.Lesson.color == color):
        if db_lesson.chosen_classroom != "" and db_lesson.chosen_classroom == chosen_cl:
            can_change = False
            break
        if dict_te.get(db_lesson.__dict__["lesson_id"]) != None:
            for te in dict_te.get(db_lesson.__dict__["lesson_id"]):
                if dict_les_te.get(te):
                    can_change = False
                    break
        if not can_change:
            break
        
        if dict_gr.get(db_lesson.__dict__["lesson_id"]):
            for gr in dict_gr.get(db_lesson.__dict__["lesson_id"]):
                if dict_les_gr.get(gr):
                    can_change = False
                    break
        if not can_change:
            break
    
    if can_change:
        db_ls = db.query(models.Lesson).filter(models.Lesson.lesson_id == lesson_id).first()
        db_ls.color = color
        db_ls.time = new_time
        db.commit()
        db.refresh(db_ls)
        return db_ls
    raise HTTPException(status_code=400, detail="The lesson cannot be added to this time!")
        

def delete_lesson(db: Session, lesson_id: str):
    for u in db.query(models.Relation_lesson_teacher).filter(models.Relation_lesson_teacher.lesson_id == lesson_id).all():
        db.delete(u)
    for u in db.query(models.Relation_lesson_group).filter(models.Relation_lesson_group.lesson_id == lesson_id).all():
        db.delete(u)
    for u in db.query(models.Relation_lesson_classroom).filter(models.Relation_lesson_classroom.lesson_id == lesson_id).all():
        db.delete(u)
    lesson = db.query(models.Lesson).filter(models.Lesson.lesson_id == lesson_id).first()
    db.delete(lesson)
    db.commit()
    return 

def delete_all_lessons(db: Session):
    db.query(models.Lesson).delete()
    db.query(models.Relation_lesson_group).delete()
    db.query(models.Relation_lesson_teacher).delete()
    db.query(models.Relation_lesson_classroom).delete()
    db.commit()
    return
    
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
        setattr(db_item, "nonpermitted_colors", new_item.nonpermitted_colors)
        db.commit()
        db.refresh(db_item)
        return db_item
    raise HTTPException(status_code=404, detail= name + " not found")
    
def create_item(db:Session, item: schemas.ItemBase, name: str):
    item_model = getattr(models, name)
    db_item = item_model()
    setattr(db_item, name.lower()+"_id", item.id)
    setattr(db_item, name.lower()+"_name", item.name)
    setattr(db_item, "nonpermitted_colors", item.nonpermitted_colors)
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

def delete_all_item(db: Session, name:str):
    item_model = getattr(models, name)
    for db_item in db.query(item_model).all():
        db.delete(db_item)

    item_relation_model = getattr(models, "Relation_lesson_" + name.lower())
    for db_rela in db.query(item_relation_model).all():
        db.delete(db_rela)
    db.commit()
