from typing import List, Optional

from sqlalchemy.sql.expression import true

from pydantic import BaseModel

# base classes
class LessonBase(BaseModel):
    lesson_id: str
    subject_id: Optional[str] = None
    subject_name: Optional[str] = None
    topic_id: Optional[str] = None
    topic_name: Optional[str] = None
    master_id: Optional[str] = None
    color: Optional[str] = None
    chosen_classroom: Optional[str] = None
    nonpermitted_colors: Optional[str] = None
    time: Optional[str] = None

class ItemBase(BaseModel):
    id: str
    name: Optional[str] = None
    nonpermitted_colors: Optional[str] = None

class GroupBase(BaseModel):
    group_id: str
    group_name: Optional[str] = None 
    nonpermitted_colors: Optional[str] = None

class TeacherBase(BaseModel):
    teacher_id: str 
    teacher_name: Optional[str] = None 
    nonpermitted_colors: Optional[str] = None

class ClassroomBase(BaseModel):
    classroom_id: str
    classroom_name: Optional[str] = None 
    nonpermitted_colors: Optional[str] = None

######################################################
# Classes for representing lesson
class Lesson_id(BaseModel):
    lesson_id: str

    class Config:
        orm_mode = True

# represent group names for lesson
class Group_n(BaseModel):
    group_name: str
    group_id: str
    class Config:
        orm_mode = True

class Group_name(BaseModel):
    group: Group_n
    class Config:
        orm_mode = True

# represent teacher names for lesson
class Teacher_n(BaseModel):
    teacher_name: str
    teacher_id: str
    class Config:
        orm_mode = True

class Teacher_name(BaseModel):
    teacher: Teacher_n
    class Config:
        orm_mode = True

# represent classroom names for lesson
class Classroom_n(BaseModel):
    classroom_name: str
    classroom_id: str
    class Config:
        orm_mode = True

class Classroom_name(BaseModel):
    classroom: Classroom_n
    class Config:
        orm_mode = True

#######################################################
# classes for creating instances of relation tables
class Relation_lesson_group(BaseModel):
    lesson_id:  str
    group_id: str

    class Config:
        orm_mode = True

class Relation_lesson_teacher(BaseModel):
    lesson_id: str
    teacher_id: str

    class Config:
        orm_mode = True

class Relation_lesson_classroom(BaseModel):
    lesson_id: str
    classroom_id: str

    class Config:
        orm_mode = True

####################################################
# classes for displaying data
# display lessons
class Lesson(LessonBase):
    groups: List[Group_name] = []
    teachers: List[Teacher_name] = []
    classrooms: List[Classroom_name] = []
    class Config:
        orm_mode = True

# display groups
class Group(GroupBase):
    lessons: List[Lesson_id] = []
    class Config:
        orm_mode = True

# display teachers
class Teacher(TeacherBase):
    lessons: List[Lesson_id] = []
    class Config:
        orm_mode = True

# display classrooms
class Classroom(ClassroomBase):
    lessons: List[Lesson_id] = []
    class Config:
        orm_mode = True

########################################################
# class for creating lesson
class Create_lesson(BaseModel):
    lesson: LessonBase
    group_ids: List[str]
    teacher_ids: List[str]
    classroom_ids: List[str]

########################################################
# class for updating colors
class Update_color(BaseModel):
    lesson_id: str
    color: str
    chosen_classroom: str
    time:str
