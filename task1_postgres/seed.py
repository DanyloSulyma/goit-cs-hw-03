import random
import psycopg2
from psycopg2 import DatabaseError
from faker import Faker

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

fake = Faker('uk_UA')

def seed_database(num_users=10, num_tasks=30):
    """Заповнює базу даних фейковими даними."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # 1. Генерація та вставка користувачів
                users_data = []
                for _ in range(num_users):
                    users_data.append((fake.name(), fake.unique.email()))
                
                cur.executemany(
                    "INSERT INTO users (fullname, email) VALUES (%s, %s);",
                    users_data
                )

                # Отримання згенерованих ID користувачів та статусів
                cur.execute("SELECT id FROM users;")
                user_ids = [row[0] for row in cur.fetchall()]

                cur.execute("SELECT id FROM status;")
                status_ids = [row[0] for row in cur.fetchall()]

                # 2. Генерація та вставка завдань
                tasks_data = []
                for _ in range(num_tasks):
                    title = fake.sentence(nb_words=4).rstrip('.')
                    # Деякі завдання навмисно залишаємо без опису (None / NULL)
                    description = fake.paragraph(nb_sentences=2) if random.random() > 0.25 else None
                    status_id = random.choice(status_ids)
                    user_id = random.choice(user_ids)
                    tasks_data.append((title, description, status_id, user_id))

                cur.executemany(
                    """
                    INSERT INTO tasks (title, description, status_id, user_id)
                    VALUES (%s, %s, %s, %s);
                    """,
                    tasks_data
                )

                conn.commit()
                print(f" Базу успішно заповнено: {num_users} користувачів, {num_tasks} завдань.")

    except DatabaseError as error:
        print(f" Помилка сидингу бази даних: {error}")

if __name__ == "__main__":
    seed_database()