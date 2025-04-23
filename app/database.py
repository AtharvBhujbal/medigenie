import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os
from app.log import logger
import psycopg2.extras

class Database:
    def __init__(self):
        self.db = psycopg2.connect(
                    dbname=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASS'),
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT')
                )
        
    def initialize_database(self):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            query = """
                DROP TABLE IF EXISTS consultation_record CASCADE;
                DROP TABLE IF EXISTS doctor CASCADE;
                DROP TABLE IF EXISTS organization_user_map CASCADE;
                DROP TABLE IF EXISTS organization CASCADE;
                DROP TABLE IF EXISTS app_user CASCADE;

                CREATE TABLE IF NOT EXISTS app_user (
                    user_id VARCHAR(32) PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(10) UNIQUE NOT NULL,
                    aadhaar_number VARCHAR(20),
                    dob DATE,
                    gender VARCHAR(10),
                    chronic_diseases TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS organization (
                    organization_id VARCHAR(32) PRIMARY KEY,
                    organization_name VARCHAR(100) NOT NULL,
                    license_no VARCHAR(50) UNIQUE NOT NULL,
                    address TEXT,
                    contact_number VARCHAR(15),
                    admin_id VARCHAR(32) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (admin_id) REFERENCES app_user(user_id)
                );

                CREATE TABLE IF NOT EXISTS organization_user_map (
                    id SERIAL PRIMARY KEY,
                    organization_id VARCHAR(32) NOT NULL,
                    user_id VARCHAR(32) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (organization_id) REFERENCES organization(organization_id),
                    FOREIGN KEY (user_id) REFERENCES app_user(user_id)
                );

                CREATE TABLE IF NOT EXISTS doctor (
                    doctor_id VARCHAR(32) PRIMARY KEY,
                    user_id VARCHAR(32) NOT NULL,
                    organization_id VARCHAR(32) NOT NULL,
                    specialization VARCHAR(100),
                    license_number VARCHAR(50) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES app_user(user_id),
                    FOREIGN KEY (organization_id) REFERENCES organization(organization_id)
                );

                CREATE TABLE IF NOT EXISTS consultation_record (
                    record_id SERIAL PRIMARY KEY,
                    patient_id VARCHAR(32) NOT NULL,
                    doctor_id VARCHAR(32) NOT NULL,
                    organization_id VARCHAR(32) NOT NULL,
                    top_5_disease TEXT[],
                    prescribed_medicine TEXT[],
                    transcribe_summary TEXT,
                    consultation_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES app_user(user_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
                    FOREIGN KEY (organization_id) REFERENCES organization(organization_id)
                );

            """
            cur.execute(query)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database Error while Initializing: {e}")
            raise 
        finally:
            cur.close()

    def create_user(self, user_id, email, password_hash, name, phone_number):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            query = """
                INSERT INTO app_user (user_id, email, password_hash, name, phone_number)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING user_id;
            """
            cur.execute(query, (user_id, email, password_hash, name, phone_number,))
            user_id = cur.fetchone()['user_id']
            self.db.commit()
            return user_id
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database Error: {e}")
            raise
        finally:
            cur.close()

    def get_user_by_email(self, email):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            query = "SELECT * FROM app_user WHERE email = %s"
            cur.execute(query, (email,))
            user = cur.fetchone()
            return user
        except Exception as e:
            logger.error(f"Database Error: {e}")
            raise
        finally:
            cur.close()


db = Database()