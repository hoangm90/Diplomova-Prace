from database import SessionLocal, engine
import models

def get_lessons():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    lessons = []
    groups = {}
    teachers = {}
    classrooms = {}
    for u in db.query(models.Relation_lesson_group).all():
        lesson_id = u.__dict__["lesson_id"]
        group_id = u.__dict__["group_id"]
        if groups.get(lesson_id) == None:
            groups[lesson_id] = []
        group = {"group_id": group_id}
        groups[lesson_id].append(group)

    for u in db.query(models.Relation_lesson_classroom).all():
        lesson_id = u.__dict__["lesson_id"]
        classroom_id = u.__dict__["classroom_id"]
        if classrooms.get(lesson_id) == None:
            classrooms[lesson_id] = []
        classroom = {"classroom_id": classroom_id}
        classrooms[lesson_id].append(classroom)

    for u in db.query(models.Relation_lesson_teacher).all():
        lesson_id = u.__dict__["lesson_id"]
        teacher_id = u.__dict__["teacher_id"]
        if teachers.get(lesson_id) == None:
            teachers[lesson_id] = []
        teacher = {"teacher_id": teacher_id}
        teachers[lesson_id].append(teacher)

    for u in db.query(models.Lesson).all():
        lesson_id = u.__dict__["lesson_id"]
        subject_id = u.__dict__["subject_id"]
        subject_name = u.__dict__["subject_name"]
        topic_id = u.__dict__["topic_id"]
        topic_name = u.__dict__["topic_name"]
        color = u.__dict__["color"]
        time = u.__dict__["time"]
        chosen_classroom = u.__dict__["chosen_classroom"]
        nonpermitted_colors = u.__dict__["nonpermitted_colors"]
        lesson = {
            "lesson_id": lesson_id,
            "subject_id": subject_id,
            "subject_name": subject_name,
            "topic_id": topic_id,
            "topic_name": topic_name,
            "color": color,
            "time": time,
            "chosen_classroom": chosen_classroom,
            "nonpermitted_colors": nonpermitted_colors,
            "groups": groups.get(lesson_id) if groups.get(lesson_id) != None else [],
            "teachers": teachers.get(lesson_id) if teachers.get(lesson_id) != None else [],
            "classrooms": classrooms.get(lesson_id) if classrooms.get(lesson_id) != None else [],
        }
        lessons.append(lesson)
    db.close()
    return lessons

def get_lessons_with_names():
    lessons_raw = get_lessons()
    lessons = []
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    groups = {}
    teachers = {}
    classrooms = {}
    
    for u in db.query(models.Group).all():
        groups[u.__dict__['group_id']] = u.__dict__['group_name']
    
    for u in db.query(models.Teacher).all():
        teachers[u.__dict__['teacher_id']] = u.__dict__['teacher_name']

    for u in db.query(models.Classroom).all():
        classrooms[u.__dict__['classroom_id']] = u.__dict__['classroom_name']
    
    db.close()

    for ls in lessons_raw:
        lesson = {
            "lesson_id": ls["lesson_id"],
            "subject_id": ls["subject_id"],
            "subject_name": ls["subject_name"],
            "topic_id": ls["topic_id"],
            "topic_name": ls["topic_name"],
            "nonpermitted_colors": ls["nonpermitted_colors"],
            "color": ls["color"],
            "time": ls["time"],
            "chosen_classroom": classrooms.get(ls["chosen_classroom"]),
            "chosen_classroom_id": ls["chosen_classroom"],
            "groups": [],
            "group_ids": [],
            "teachers": [],
            "teacher_ids": [],
            "classrooms": [],
            "classroom_ids": [],
        }

        for group_id in ls["groups"]:
            lesson["groups"].append(groups[group_id["group_id"]])
            lesson["group_ids"].append(group_id["group_id"])
        
        for teacher_id in ls["teachers"]:
            lesson["teachers"].append(teachers[teacher_id["teacher_id"]])
            lesson["teacher_ids"].append(teacher_id["teacher_id"])
        
        for classroom_id in ls["classrooms"]:
            lesson["classrooms"].append(classrooms[classroom_id["classroom_id"]])
            lesson["classroom_ids"].append(classroom_id["classroom_id"])
        
        lessons.append(lesson)
    
    return lessons
    
def get_items(name: str):
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    model_name = getattr(models, name)
    items_obj = db.query(model_name).all()
    items = []
    item_id = name.lower() + "_id"
    item_name = name.lower() + "_name"
    for item in items_obj:
        items.append({
            item_id: item.__dict__[item_id],
            item_name: item.__dict__[item_name],
            "nonpermitted_colors": item.__dict__["nonpermitted_colors"],
        })
    db.close()
    return items

def get_items_with_lessons(name: str):
    items = get_items(name)
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    lessons = {}
    for u in db.query(models.Lesson).all():
        lessons[u.__dict__["lesson_id"]] = u.__dict__["subject_name"]

    item_lessons = {}
    item_id = name.lower() + "_id"
    model_relation_item = getattr(models, "Relation_lesson_" + name.lower())
    for u in db.query(model_relation_item).all():
        if item_lessons.get(u.__dict__[item_id]) == None:
            item_lessons[u.__dict__[item_id]] = set()
        lesson_name = lessons[u.__dict__["lesson_id"]]
        item_lessons[u.__dict__[item_id]].add(lesson_name)
    
    for i in range(len(items)):
        items[i]["lesson"] = item_lessons.get(items[i][item_id]) if item_lessons.get(items[i][item_id]) != None else set()
    return items

if __name__ == "__main__":
    print(get_lessons_with_names())