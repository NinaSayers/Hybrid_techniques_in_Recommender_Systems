from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base
from data_access.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
