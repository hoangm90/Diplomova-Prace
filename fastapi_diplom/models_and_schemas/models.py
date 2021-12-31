from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import true

from manage_database.database import Base

########################################################################
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=true, index=true)
    lesson_id = Column(String, unique=true, index=true)
    subject_id = Column(String)
    subject_name = Column(String)
    topic_id = Column(String)
    topic_name = Column(String)
    master_id = Column(String)
    color = Column(Integer)
    chosen_classroom = Column(String)
    nonpermitted_colors = Column(String)
    time = Column(String)

    groups = relationship("Relation_lesson_group", back_populates="lesson")
    teachers = relationship("Relation_lesson_teacher", back_populates="lesson")
    classrooms = relationship("Relation_lesson_classroom", back_populates="lesson")

########################################################################
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=true, index=true)
    group_id = Column(String, unique=true, index=true)
    group_name = Column(String)
    nonpermitted_colors = Column(String)

    lessons = relationship("Relation_lesson_group", back_populates="group")

########################################################################
class Relation_lesson_group(Base):
    __tablename__ = "relation lesson and group"

    id = Column(Integer, primary_key=true, index=true)
    lesson_id = Column(String, ForeignKey("lessons.lesson_id"))
    group_id = Column(String, ForeignKey("groups.group_id"))

    lesson = relationship("Lesson", back_populates="groups")
    group = relationship("Group", back_populates="lessons")

########################################################################
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=true, index=true)
    teacher_id = Column(String, unique=true, index=true)
    teacher_name = Column(String)
    nonpermitted_colors = Column(String)

    lessons = relationship("Relation_lesson_teacher", back_populates="teacher")

########################################################################
class Relation_lesson_teacher(Base):
    __tablename__ = "relation lesson and teacher"

    id = Column(Integer, primary_key=true, index=true)
    lesson_id = Column(String, ForeignKey("lessons.lesson_id"))
    teacher_id = Column(String, ForeignKey("teachers.teacher_id"))
   
    teacher = relationship("Teacher", back_populates="lessons")
    lesson = relationship("Lesson", back_populates="teachers")

########################################################################
class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=true, index=true)
    classroom_id = Column(String, unique=true, index=true)
    classroom_name = Column(String)
    nonpermitted_colors = Column(String)

    lessons = relationship("Relation_lesson_classroom", back_populates="classroom")

########################################################################
class Relation_lesson_classroom(Base):
    __tablename__ = "relation lesson and classroom"

    id = Column(Integer, primary_key=true, index=true)
    lesson_id = Column(String, ForeignKey("lessons.lesson_id"))
    classroom_id = Column(String, ForeignKey("classrooms.classroom_id"))
   
    classroom = relationship("Classroom", back_populates="lessons")
    lesson = relationship("Lesson", back_populates="classrooms")