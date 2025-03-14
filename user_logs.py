import sqlite3


def get_event_type_ids(event_types: list[str]) -> dict[str, int]:
    """
    Получает ID событий (login, logout и т.д.) по их названию.
    """
    try:
        with sqlite3.connect("logs_database.db") as connection:
            cursor = connection.cursor()
            # Приводим названия событий к нижнему регистру
            event_types_lower = [event.lower() for event in event_types]
            query = f"""
            SELECT id, name FROM event_type 
            WHERE LOWER(name) IN ({",".join("?" * len(event_types_lower))})
            """
            cursor.execute(query, event_types_lower)
            return {name: event_id for event_id, name in cursor.fetchall()}

    except sqlite3.Error:
        return {}


def get_space_type_ids(space_types: list[str]) -> dict[str, int]:
    """
    Получает ID пространств (blog, post и т.д.) по их названию.
    """
    try:
        with sqlite3.connect("logs_database.db") as connection:
            cursor = connection.cursor()
            # Приводим названия пространств к нижнему регистру
            space_types_lower = [space.lower() for space in space_types]
            query = f"""
            SELECT id, name FROM space_type 
            WHERE LOWER(name) IN ({",".join("?" * len(space_types_lower))})
            """
            cursor.execute(query, space_types_lower)
            return {name: space_id for space_id, name in cursor.fetchall()}

    except sqlite3.Error:
        return {}


def get_event_count_by_type(event_ids: list[int], datetime: str) -> dict[int, int]:
    """
    Получает количество событий (login, logout) в указанную дату.
    """
    try:
        with sqlite3.connect("logs_database.db") as connection:
            cursor = connection.cursor()
            query = f"""
            SELECT event_type_id, COUNT(*) FROM logs
            WHERE event_type_id IN ({",".join("?" * len(event_ids))})
            AND datetime LIKE ?
            GROUP BY event_type_id
            """
            cursor.execute(query, event_ids + [f"{datetime}%"])
            return {event_type_id: count for event_type_id, count in cursor.fetchall()}

    except sqlite3.Error:
        return {}


def get_blog_activity_count(date: str) -> int:
    """
    Получает количество действий внутри блога за указанную дату.
    """
    try:
        with sqlite3.connect("logs_database.db") as connection:
            cursor = connection.cursor()

            # Получаем ID для пространства "blog"
            blog_space_id = get_space_type_ids(["blog"]).get("blog")
            if blog_space_id is None:
                return 0

            query = """
            SELECT COUNT(*) FROM logs
            WHERE space_type_id = ?
            AND datetime LIKE ?
            """
            cursor.execute(query, (blog_space_id, f"{date}%"))
            result = cursor.fetchone()
            return result[0] if result else 0

    except sqlite3.Error:
        return 0


def get_user_activity_by_date(datetime: str) -> dict:
    """
    Формирует итоговый дата-сет с общей информацией о действиях пользователя.
    """
    # Получаем ID событий "login" и "logout"
    event_types = get_event_type_ids(["login", "logout"])

    login_even_type = event_types.get("login")
    logout_even_type = event_types.get("logout")
    login_count = get_event_count_by_type([login_even_type], datetime).get(login_even_type, 0)
    logout_count = get_event_count_by_type([logout_even_type], datetime).get(logout_even_type, 0)
    blog_activity_count = get_blog_activity_count(datetime)

    return {
        "date": datetime,
        "logins": login_count,
        "logouts": logout_count,
        "blog_activity": blog_activity_count
    }


if __name__ == "__main__":
    date = "2023-10-01"
    result = get_user_activity_by_date(date)
    print(result)
