import psycopg2
from psycopg2 import Error
from config import PG_DB_CONFIG
from colorama import init, Fore, Style

# Ініціалізація colorama
init(autoreset=True)

def create_connection():
    """Створення з'єднання з PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(**PG_DB_CONFIG)
        return conn
    except Exception as e:
        print(f"{Fore.RED} Connection error: {e}")
        return None
    finally:
        pass


def create_table(conn, create_table_sql):
    """Створення таблиці на основі переданого SQL-запиту."""
    try:
        with conn.cursor() as cursor:
            print(f"{Fore.YELLOW}Executing SQL: {create_table_sql}")  # Логування SQL запиту
            cursor.execute(create_table_sql)
            conn.commit()  # Це явно фіксує зміни в базі даних
        print(f"{Fore.GREEN}The table was created successfully.")
    except Error as e:
        print(f"{Fore.RED}Error creating table: {e}")


if __name__ == "__main__":
    # SQL-запити для створення таблиці users
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE
    );
    """
    # SQL-запити для створення таблиці statuses
    sql_create_statuses_table = """
    CREATE TABLE IF NOT EXISTS statuses (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    """
    # SQL-запити для створення таблиці tasks
    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER REFERENCES statuses(id),
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
    """

    # Підключення до бази даних і створення таблиць
    conn = create_connection()
    if conn:
        print(f"{Fore.GREEN}The connection to the database is successful.")
        print(f"{Fore.BLUE}Creating the 'users' table...")
        create_table(conn, sql_create_users_table)

        print(f"{Fore.BLUE}Creating the 'statuses' table...")
        create_table(conn, sql_create_statuses_table)

        print(f"{Fore.BLUE}Creating the 'tasks' table...")
        create_table(conn, sql_create_tasks_table)

        conn.close()

        print(f"{Fore.GREEN}All tables have been created successfully!")
    else:
        print(f"{Fore.RED}A database connection could not be established.")
