import psycopg2
from colorama import init, Fore
import faker
from random import randint, choice
from config import PG_DB_CONFIG

# Ініціалізація colorama для кольорового виводу
init(autoreset=True)

# Додавання статусів
all_statuses = ['new', 'in progress', 'completed']
number_of_users = 15
number_of_tasks = 30


def create_connection():
    # Створення з'єднання з PostgreSQL.
    conn = None
    try:
        conn = psycopg2.connect(**PG_DB_CONFIG)
        return conn
    except Exception as e:
        print(f"{Fore.RED}Connection error: {e}")

def generate_email(fake, domains):
    # Генерує електронну адресу з обраним доменом.
    username = fake.user_name()  # Генерує ім'я користувача
    domain = choice(domains)  # Випадковий вибір домену зі списку
    return f"{username}@{domain}"

def generate_fake_data(users_count, tasks_count):
    # Генерація фейкових даних для заповнення таблиць.
    fake = faker.Faker()
    allowed_domains = ["ukr.net", "gmail.com"]  # Список дозволених доменів

    fake_users = [
        {"fullname": fake.name(), "email": generate_email(fake, allowed_domains)}
        for _ in range(users_count)
    ]
    fake_tasks = [
        {
            "title": fake.sentence(),
            "description": fake.text(),
            "status_id": randint(1, len(all_statuses)),
            "user_id": randint(1, users_count),
        }
        for _ in range(tasks_count)
    ]

    return fake_users, fake_tasks


def prepare_data(users, statuses, tasks):
    # Підготовка даних до вставки в таблиці.
    for_users = [(user["fullname"], user["email"]) for user in users]
    for_statuses = [(status,) for status in statuses]
    for_tasks = [
        (task["title"], task["description"], task["status_id"], task["user_id"])
        for task in tasks
    ]
    return for_users, for_statuses, for_tasks


def insert_data_to_db(users, statuses, tasks):
    # Вставка даних у таблиці БД.
    conn = create_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()

        # Вставка користувачів
        add_users = """
        INSERT INTO users (fullname, email) VALUES (%s, %s)
        ON CONFLICT (email) DO NOTHING;
        """
        cur.executemany(add_users, users)
        print(f"{Fore.GREEN}Users added successfully.")

        # Вставка статусів
        add_statuses = """
        INSERT INTO statuses (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
        """
        cur.executemany(add_statuses, statuses)
        print(f"{Fore.GREEN}Statuses added successfully.")

        # Вставка завдань
        add_tasks = """
        INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);
        """
        cur.executemany(add_tasks, tasks)
        print(f"{Fore.GREEN}Tasks successfully added.")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"{Fore.RED}Error inserting data: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    print(f"{Fore.YELLOW}Data generation...")
    users, tasks = generate_fake_data(number_of_users, number_of_tasks)
    users, statuses, tasks = prepare_data(users, all_statuses, tasks)

    print(f"{Fore.YELLOW}Filling the database...")
    insert_data_to_db(users, statuses, tasks)
    print(f"{Fore.BLUE}The database is successfully populated!")