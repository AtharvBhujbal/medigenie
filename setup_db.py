from app.database import db
from app.redis import cache
from app.user import User

if __name__ == "__main__":
    input("This will initialize the database. Press Enter to continue...")
    db.initialize_database()
    cache.flush()
    print("Database Initialized")
    print("Creating admin user......")
    admin = User(
        email="admin@medigenie.in",
        password="Medigenie@2025",
        name= "Admin",
        is_admin= True,
        phone_number="1234567890"
    )
    admin.register()
    print("Admin created Successfully")