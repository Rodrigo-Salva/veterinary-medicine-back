from sqlalchemy import create_engine, inspect
import os
import sys

# Add the current directory to sys.path to import settings
sys.path.append(os.getcwd())

try:
    from app.infrastructure.config.settings import settings
    engine = create_engine(settings.DATABASE_URL)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in DB: {', '.join(tables)}")
except Exception as e:
    print(f"Error checking tables: {e}")
