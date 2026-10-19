import sys
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Рядок підключення з вашими даними MongoDB Atlas
MONGO_URI = ""
DB_NAME = "cat_database"
COLLECTION_NAME = "cats"


def get_collection():
    """Створює та повертає об'єкт колекції MongoDB."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


# ==========================================
# 1. СТВОРЕННЯ (CREATE / SEED)
# ==========================================
def seed_cats() -> None:
    """Заповнює колекцію початковими документами про котів."""
    col = get_collection()
    initial_cats = [
        {
            "name": "barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"]
        },
        {
            "name": "murzik",
            "age": 5,
            "features": ["спить цілий день", "чорний"]
        },
        {
            "name": "vaska",
            "age": 2,
            "features": ["білий", "полюбляє рибу"]
        }
    ]
    try:
        col.delete_many({})  # Попереднє очищення для повторного запуску
        result = col.insert_many(initial_cats)
        print(f"Початкові дані додано. Генерувані ID: {result.inserted_ids}")
    except PyMongoError as e:
        print(f"Помилка під час ініціалізації даних: {e}")


# ==========================================
# 2. ЧИТАННЯ (READ)
# ==========================================
def get_all_cats() -> None:
    """Виводить усі записи з колекції котів."""
    col = get_collection()
    try:
        cats = list(col.find())
        print("\n--- Список усіх котів у базі ---")
        if not cats:
            print("База даних порожня.")
            return
        for cat in cats:
            print(f"ID: {cat['_id']} | Назва: {cat.get('name')} | Вік: {cat.get('age')} | Характеристики: {cat.get('features')}")
    except PyMongoError as e:
        print(f"Помилка при отриманні списку котів: {e}")


def get_cat_by_name(name: str) -> None:
    """Знаходить та виводить інформацію про кота за його ім'ям."""
    col = get_collection()
    try:
        cat = col.find_one({"name": name})
        print(f"\n--- Пошук кота '{name}' ---")
        if cat:
            print(f"Знайдено: {cat}")
        else:
            print(f"Кот з ім'ям '{name}' відсутній у базі.")
    except PyMongoError as e:
        print(f"Помилка під час пошуку кота: {e}")


# ==========================================
# 3. ОНОВЛЕННЯ (UPDATE)
# ==========================================
def update_cat_age(name: str, new_age: int) -> None:
    """Оновлює вік кота за вказаним ім'ям."""
    col = get_collection()
    try:
        result = col.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"\nВік кота '{name}' оновлено до {new_age} р.")
        else:
            print(f"\nНе вдалося оновити вік кота '{name}' (можливо, ім'я не знайдено або вік не змінився).")
    except PyMongoError as e:
        print(f"Помилка при оновленні віку: {e}")
ongodb+srv://danulo007_db_user:FSbSaNP4rzDg1ToR@cluster0.rsn6odn.mongodb.net/?retryWrites=true&w=majorit

def add_cat_feature(name: str, new_feature: str) -> None:
    """Додає нову характеристику до списку features кота за ім'ям."""
    col = get_collection()
    try:
        # $addToSet гарантує відсутність дублікатів у списку features
        result = col.update_one({"name": name}, {"$addToSet": {"features": new_feature}})
        if result.modified_count > 0:
            print(f"\nХарактеристику '{new_feature}' додано коту '{name}'.")
        else:
            print(f"\nНе вдалося додати характеристику коту '{name}' (можливо, така характеристика вже є).")
    except PyMongoError as e:
        print(f"Помилка при додаванні характеристики: {e}")


# ==========================================
# 4. ВИДАЛЕННЯ (DELETE)
# ==========================================
def delete_cat_by_name(name: str) -> None:
    """Видаляє запис про кота з колекції за його ім'ям."""
    col = get_collection()
    try:
        result = col.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"\nЗапис про кота '{name}' успішно видалено.")
        else:
            print(f"\nКот з ім'ям '{name}' не знайдений для видалення.")
    except PyMongoError as e:
        print(f"Помилка при видаленні кота: {e}")


def delete_all_cats() -> None:
    """Видаляє всі записи з колекції."""
    col = get_collection()  # <--- Допишіть _collection()
    try:
        result = col.delete_many({})
        print(f"\nУсі записи видалено! Очищено документів: {result.deleted_count}.")
    except PyMongoError as e:
        print(f"Помилка при очищенні колекції: {e}")

if __name__ == "__main__":
    print("=== ЗАПУСК СКРИПТА PYMONGO ===")
    seed_cats()
    get_all_cats()
    get_cat_by_name("barsik")
    update_cat_age("barsik", 4)
    add_cat_feature("barsik", "люб'язний")
    get_cat_by_name("barsik")
    delete_cat_by_name("murzik")
    get_all_cats()
    delete_all_cats()
    get_all_cats()