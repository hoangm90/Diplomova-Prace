from manage_database.database import SessionLocal, engine
from typing import List
from models_and_schemas import schemas, models

def update_color(lesson_color_class: List[schemas.Update_color]):
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    dict_lesson_color = {}
    dict_lesson_class = {}
    dict_lesson_time = {}
    for lesson in lesson_color_class:
        dict_lesson_color[lesson["lesson_id"]] = lesson["color"]
        dict_lesson_class[lesson["lesson_id"]] = lesson["chosen_classroom"]
        dict_lesson_time[lesson["lesson_id"]] = lesson["time"]
    db_lessons = db.query(models.Lesson).all()
    for db_lesson in db_lessons:
        db_lesson.color = dict_lesson_color[db_lesson.lesson_id]
        db_lesson.chosen_classroom = dict_lesson_class[db_lesson.lesson_id]
        db_lesson.time = dict_lesson_time[db_lesson.lesson_id]
    db.commit()
    db.close()
    return