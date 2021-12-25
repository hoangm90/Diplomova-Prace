from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import groups, teachers, classrooms, lessons

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