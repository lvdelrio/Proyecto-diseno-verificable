from database import engine, Base
from model.user import User

print("Creating tables...")
Base.metadata.create_all(engine)
print("Tables created successfully!")