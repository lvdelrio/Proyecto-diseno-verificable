from sqlalchemy import create_engine as ce
from sqlalchemy.orm import declarative_base, sessionmaker
#cambiar url de base de datos
DATABASE_URL = "mysql+mysqlconnector://root:password@localhost"
file_db = ce(DATABASE_URL)

db_name = "my_database"

with file_db.connect() as conn:
    conn.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")

Base = declarative_base()
SessionLocal = sessionmaker(bind=file_db)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
