import sqlite3


def create_authors_database():
    """Создает базу данных authors_database1.db с таблицами users, blog, post и comment."""
    try:
        with sqlite3.connect("authors_database1.db") as connection:
            cursor = connection.cursor()

            # Создание таблицы users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    login TEXT UNIQUE NOT NULL
                )
            """)

            # Создание таблицы blog
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    FOREIGN KEY (owner_id) REFERENCES users(id)
                )
            """)

            # Создание таблицы post
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS post (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    header TEXT NOT NULL,
                    text TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    blog_id INTEGER NOT NULL,
                    FOREIGN KEY (author_id) REFERENCES users(id),
                    FOREIGN KEY (blog_id) REFERENCES blog(id)
                )
            """)

            # Создание таблицы comment
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    FOREIGN KEY (post_id) REFERENCES post(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

            print("База данных authors_database1.db успешно создана.")

    except sqlite3.Error as e:
        print(f"Ошибка при создании authors_database1.db: {e}")


def create_logs_database():
    """Создает базу данных logs_database1.db с таблицами space_type, event_type и logs."""
    try:
        with sqlite3.connect("logs_database1.db") as connection:
            cursor = connection.cursor()

            # Создание таблицы space_type
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS space_type (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)

            # Создание таблицы event_type
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS event_type (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)

            # Создание таблицы logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    space_type_id INTEGER NOT NULL,
                    event_type_id INTEGER NOT NULL,
                    FOREIGN KEY (space_type_id) REFERENCES space_type(id),
                    FOREIGN KEY (event_type_id) REFERENCES event_type(id)
                )
            """)

            print("База данных logs_database1.db успешно создана.")

    except sqlite3.Error as e:
        print(f"Ошибка при создании logs_database1.db: {e}")


def insert_test_data():
    """Заполняет базы данных тестовыми данными."""
    try:
        with sqlite3.connect("authors_database1.db") as connection:
            cursor = connection.cursor()

            # Добавление тестовых пользователей
            cursor.executemany(
                "INSERT INTO users (email, login) VALUES (?, ?)",
                [
                    ("user1@example.com", "user1"),
                    ("user2@example.com", "user2"),
                    ("author1@example.com", "author1"),
                    ("author2@example.com", "author2"),
                ],
            )

            # Добавление тестовых блогов
            cursor.executemany(
                "INSERT INTO blog (owner_id, name, description) VALUES (?, ?, ?)",
                [
                    (1, "Blog 1", "Description of Blog 1"),
                    (2, "Blog 2", "Description of Blog 2"),
                ],
            )

            # Добавление тестовых постов
            cursor.executemany(
                "INSERT INTO post (header, text, author_id, blog_id) VALUES (?, ?, ?, ?)",
                [
                    ("Post 1", "This is the content of Post 1", 3, 1),
                    ("Post 2", "This is the content of Post 2", 4, 2),
                    ("Post 3", "This is the content of Post 3", 3, 1),
                ],
            )

            # Добавление тестовых комментариев
            cursor.executemany(
                "INSERT INTO comment (post_id, user_id, text) VALUES (?, ?, ?)",
                [
                    (1, 1, "Great post!"),
                    (1, 2, "I agree with this post."),
                    (2, 1, "Nice work!"),
                    (3, 2, "Interesting read."),
                    (3, 1, "Thanks for sharing."),
                ],
            )

            print("Тестовые данные для authors_database1.db успешно добавлены.")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении тестовых данных в authors_database1.db: {e}")

    try:
        with sqlite3.connect("logs_database1.db") as connection:
            cursor = connection.cursor()

            # Добавление типов пространств
            cursor.executemany(
                "INSERT INTO space_type (name) VALUES (?)",
                [("global",), ("blog",), ("post",)],
            )

            # Добавление типов событий
            cursor.executemany(
                "INSERT INTO event_type (name) VALUES (?)",
                [("login",), ("logout",), ("comment",), ("create_post",), ("delete_post",)],
            )

            # Добавление тестовых логов
            cursor.executemany(
                "INSERT INTO logs (datetime, user_id, space_type_id, event_type_id) VALUES (?, ?, ?, ?)",
                [
                    ("2023-10-01 10:00:00", 1, 1, 1),
                    ("2023-10-01 10:05:00", 1, 3, 3),
                    ("2023-10-01 10:10:00", 2, 1, 1),
                    ("2023-10-01 10:15:00", 2, 2, 4),
                    ("2023-10-01 10:20:00", 1, 1, 2),
                    ("2023-10-01 10:25:00", 2, 3, 3),
                    ("2023-10-01 10:30:00", 1, 1, 1),
                    ("2023-10-01 10:35:00", 1, 2, 5),
                ],
            )

            print("Тестовые данные для logs_database1.db успешно добавлены.")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении тестовых данных в logs_database1.db: {e}")


if __name__ == "__main__":
    # Создание баз данных
    create_authors_database()
    create_logs_database()

    # Заполнение тестовыми данными
    insert_test_data()