
import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os
from app.log import logger

class database:
    def __init__(self):
        self.db = psycopg2.connect(
                    dbname=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASS'),
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT')
                )
        
    def initialize_database(self):
        cur = self.db.cursor()
        try:
            query = """
                -- Drop tables in reverse dependency order
                DROP TABLE IF EXISTS consultation_record CASCADE;
                DROP TABLE IF EXISTS doctor CASCADE;
                DROP TABLE IF EXISTS organization_user_map CASCADE;
                DROP TABLE IF EXISTS organization CASCADE;
                DROP TABLE IF EXISTS user CASCADE;

                -- Create user table
                CREATE TABLE IF NOT EXISTS user (
                    user_id SERIAL PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(15),
                    aadhaar_number VARCHAR(20),
                    dob DATE,
                    gender VARCHAR(10),
                    chronic_diseases TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Create organization table
                CREATE TABLE IF NOT EXISTS organization (
                    organization_id SERIAL PRIMARY KEY,
                    organization_name VARCHAR(100) NOT NULL,
                    license_no VARCHAR(50) UNIQUE NOT NULL,
                    address TEXT,
                    contact_number VARCHAR(15),
                    admin_id INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (admin_id) REFERENCES user(user_id)
                );

                -- Create organization_user_map table
                CREATE TABLE IF NOT EXISTS organization_user_map (
                    id SERIAL PRIMARY KEY,
                    organization_id INT NOT NULL,
                    user_id INT NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (organization_id) REFERENCES organization(organization_id),
                    FOREIGN KEY (user_id) REFERENCES user(user_id)
                );

                -- Create doctor table
                CREATE TABLE IF NOT EXISTS doctor (
                    doctor_id SERIAL PRIMARY KEY,
                    user_id INT NOT NULL,
                    organization_id INT NOT NULL,
                    specialization VARCHAR(100),
                    license_number VARCHAR(50) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user(user_id),
                    FOREIGN KEY (organization_id) REFERENCES organization(organization_id)
                );

                -- Create consultation_record table
                CREATE TABLE IF NOT EXISTS consultation_record (
                    record_id SERIAL PRIMARY KEY,
                    patient_id INT NOT NULL,
                    doctor_id INT NOT NULL,
                    organization_id INT NOT NULL,
                    top_5_disease TEXT[],
                    prescribed_medicine TEXT[],
                    transcribe_summary TEXT,
                    consultation_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES user(user_id),
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


db = database()