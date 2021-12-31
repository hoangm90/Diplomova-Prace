from manage_database.database import SessionLocal, engine
from models_and_schemas import models 

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()