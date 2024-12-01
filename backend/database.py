from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

YOUR_PASSWORD = "ufhybnehf23"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{YOUR_PASSWORD}@localhost:5432/signing_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
