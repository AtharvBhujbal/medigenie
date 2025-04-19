from app.database import db
from app.redis import cache

if __name__ == "__main__":
    input("This will initialize the database. Press Enter to continue...")
    db.initialize_database()
    cache.flush()
    print("Database Initialized")