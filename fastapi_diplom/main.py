from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from routers import groups, teachers, classrooms, lessons
import crud 
import manage_database.dependency as dependency 
import helper_function.submitData as submitData 
import helper_function.coloring as coloring 
import helper_function.sort_lessons as sort_lessons

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# router for lessons
app.include_router(lessons.router)

# router for groups
app.include_router(groups.router)

# router for teachers
app.include_router(teachers.router)

# router for classrooms
app.include_router(classrooms.router)

# submit json file
@app.post("/", tags=["all"])
def submit_data(data: UploadFile = File(...), db: Session = Depends(dependency.get_db)):
    crud.delete_all_lessons(db)
    crud.delete_all_item(db, "Teacher")
    crud.delete_all_item(db, "Group")
    crud.delete_all_item(db, "Classroom")
    contents = data.file.read()
    submitData.submit_data(contents, db)
    coloring.update_colors_to_database()
    return sort_lessons.sort_lessons()