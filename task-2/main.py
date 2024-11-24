from pymongo import MongoClient, errors


# Підключення до MongoDB
def get_database():
    try:
        client = MongoClient("mongodb+srv://novalenkov05:20KYlVzmuOJhencr@cluster0.hhu1c.mongodb.net/DB_cats?retryWrites=true&w=majority&appName=Cluster0")  # Замініть на свій URI для MongoDB Atlas, якщо потрібно
        return client['cats_database']  # Назва вашої бази даних
    except errors.ConnectionError as e:
        print(f"Помилка підключення до MongoDB: {e}")
        return None


# Створення колекції
db = get_database()
if db is not None:
    cats_collection = db['cats']  # Назва вашої колекції

def clean_input(text):
    # Очистка тексту від проблемних символів
    return text.encode('utf-8', 'ignore').decode('utf-8')

# CRUD-функції
def create_cat(name, age, features):
    """Створення нового запису."""
    try:
        cat = {"name": name, "age": age, "features": features}
        result = cats_collection.insert_one(cat)
        print(f"Кіт успішно доданий з ID: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка створення кота: {e}")


def read_all_cats():
    """Виведення всіх записів."""
    try:
        cats = list(cats_collection.find())
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка читання записів: {e}")


def read_cat_by_name(name):
    """Знайти кота за ім'ям."""
    try:
        cat = cats_collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("Кіт із таким ім'ям не знайдений.")
    except Exception as e:
        print(f"Помилка пошуку кота: {e}")


def update_cat_age(name, new_age):
    """Оновлення віку кота."""
    try:
        result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print(f"Вік кота '{name}' успішно оновлено.")
        else:
            print("Кіт із таким ім'ям не знайдений.")
    except Exception as e:
        print(f"Помилка оновлення віку: {e}")


def add_feature_to_cat(name, feature):
    """Додавання нової характеристики до кота."""
    try:
        result = cats_collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.matched_count:
            print(f"Характеристика '{feature}' успішно додана коту '{name}'.")
        else:
            print("Кіт із таким ім'ям не знайдений.")
    except Exception as e:
        print(f"Помилка додавання характеристики: {e}")


def delete_cat_by_name(name):
    """Видалення кота за ім'ям."""
    try:
        result = cats_collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"Кіт '{name}' успішно видалений.")
        else:
            print("Кіт із таким ім'ям не знайдений.")
    except Exception as e:
        print(f"Помилка видалення кота: {e}")


def delete_all_cats():
    """Видалення всіх записів."""
    try:
        result = cats_collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів.")
    except Exception as e:
        print(f"Помилка видалення записів: {e}")


# Головна програма
def main():
    while True:
        print("\nОберіть операцію:")
        print("1. Додати нового кота")
        print("2. Вивести всіх котів")
        print("3. Знайти кота за ім'ям")
        print("4. Оновити вік кота")
        print("5. Додати характеристику коту")
        print("6. Видалити кота за ім'ям")
        print("7. Видалити всіх котів")
        print("8. Вийти")

        choice = input("Введіть номер операції: ")

        if choice == "1":
            name = input("Введіть ім'я кота: ")
            age = int(input("Введіть вік кота: "))
            features = input("Введіть характеристики кота (через кому): ").split(",")
            create_cat(name, age, [f.strip() for f in features])
        elif choice == "2":
            read_all_cats()
        elif choice == "3":
            name = input("Введіть ім'я кота: ")
            read_cat_by_name(name)
        elif choice == "4":
            name = input("Введіть ім'я кота: ")
            new_age = int(input("Введіть новий вік: "))
            update_cat_age(name, new_age)
        elif choice == "5":
            name = input("Введіть ім'я кота: ")
            feature = input("Введіть нову характеристику: ")
            add_feature_to_cat(name, feature)
        elif choice == "6":
            name = input("Введіть ім'я кота: ")
            delete_cat_by_name(name)
        elif choice == "7":
            delete_all_cats()
        elif choice == "8":
            print("Вихід із програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
