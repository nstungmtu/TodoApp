from sqlalchemy import create_engine
from models import ini_db

engine = create_engine("sqlite+pysqlite:///todo_app.db", echo=True, future=True)

ini_db(engine)

print("Database initialized successfully.")