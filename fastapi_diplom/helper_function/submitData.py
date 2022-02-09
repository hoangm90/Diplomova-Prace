from sqlalchemy.orm import Session
import json

from models_and_schemas import models

def submit_data(file: bytes, db: Session):
    data = json.loads(file)

    for teacher in data["teachers"]:
        db_teacher = models.Teacher(teacher_id=teacher["id"], teacher_name=teacher["name"])
        db.add(db_teacher)
    for classroom in data["classrooms"]:
        db_classroom = models.Classroom(classroom_id=classroom["id"], classroom_name=classroom["name"])
        db.add(db_classroom)
    for group in data["groups"]:
        db_group = models.Group(group_id=group["id"], group_name=group["name"])
        db.add(db_group)
    for lesson in data["events"]:
        if lesson.get("id") == None:
            continue
        db_lesson = models.Lesson(
            lesson_id = lesson["id"],
            subject_id = lesson.get("subjectId") if lesson.get("subjectId") != None else "",
            subject_name = lesson.get("subjectName") if lesson.get("subjectName") != None else "",
            topic_id = lesson.get("topicId") if lesson.get("topicId") != None else "",
            topic_name = lesson.get("topic") if lesson.get("topic") != None else "",
            master_id = lesson.get("masterId") if lesson.get("masterId") != None else "",
            color = -1,
            chosen_classroom = "",
            nonpermitted_colors = "",
            time = "",
        )
        db.add(db_lesson)

        for group_id in lesson["groupsIds"]:
            db_relation_lesson_group = models.Relation_lesson_group(lesson_id=lesson["id"], group_id=group_id)
            db.add(db_relation_lesson_group)
        for teacher_id in lesson["teachersIds"]:
            db_relation_lesson_teacher = models.Relation_lesson_teacher(lesson_id=lesson["id"], teacher_id=teacher_id)
            db.add(db_relation_lesson_teacher)
        for classroom_id in lesson["classroomsIds"]:
            db_relation_lesson_classroom = models.Relation_lesson_classroom(lesson_id=lesson["id"], classroom_id=classroom_id)
            db.add(db_relation_lesson_classroom)
    
    db.commit()
    return
