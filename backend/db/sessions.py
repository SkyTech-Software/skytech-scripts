from sqlalchemy.orm import sessionmaker
from backend.db.models import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
