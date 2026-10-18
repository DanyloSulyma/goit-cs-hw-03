import psycopg2
from psycopg2 import DatabaseError

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

CREATE_TABLES_SQL = """
-- Перестворення таблиць за потреби
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;

-- Таблиця користувачів
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Таблиця статусів
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Таблиця завдань
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id) ON DELETE RESTRICT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Наповнення базовими статусами
INSERT INTO status (name) VALUES 
    ('new'), 
    ('in progress'), 
    ('completed') 
ON CONFLICT (name) DO NOTHING;
"""

def create_tables():
    """Створює структуру таблиць у PostgreSQL."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLES_SQL)
                conn.commit()
                print(" Таблиці успішно створені та базові статуси додані.")
    except DatabaseError as error:
        print(f" Помилка бази даних під час створення таблиць: {error}")

if __name__ == "__main__":
    create_tables()