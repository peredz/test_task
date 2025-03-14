import sqlite3


def get_user_id_by_login(login: str) -> int | None:
    """Получает ID пользователя по логину."""
    try:
        with sqlite3.connect("authors_database.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
            user_id = cursor.fetchone()

            if not user_id:
                return None

            return user_id[0]

    except sqlite3.Error:
        return None


def get_commented_post_ids(user_id: int) -> dict[int, int]:
    """Возвращает словарь {post_id: количество комментариев} для пользователя."""
    try:
        with sqlite3.connect("authors_database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT post_id, COUNT(*) as comment_count
                FROM comment
                WHERE user_id = ?
                GROUP BY post_id
                """,
                (user_id,),
            )
            return {row[0]: row[1] for row in cursor.fetchall()}

    except sqlite3.Error:
        return {}


def get_post_details(post_ids: dict[int, int]) -> list[dict]:
    """
    Получает заголовки постов и авторов по списку post_id,
    а также количество комментариев к каждому посту.
    """
    if not post_ids:
        return []

    try:
        with sqlite3.connect("authors_database.db") as connection:
            cursor = connection.cursor()

            # Получаем информацию о постах и их авторах
            query = """
            SELECT p.id, p.header, u.login
            FROM post p
            JOIN users u ON p.author_id = u.id
            WHERE p.id IN ({})
            """.format(",".join("?" * len(post_ids)))

            cursor.execute(query, list(post_ids.keys()))
            posts = cursor.fetchall()

            return [
                {
                    "header": post[1],
                    "author_login": post[2],
                    "comments_count": post_ids[post[0]],
                }
                for post in posts
            ]

    except sqlite3.Error:
        return []


def get_comments_by_login(login: str) -> dict:
    """
    Получает все посты, к которым пользователь оставлял комментарии,
    с указанием заголовка поста, логина автора и количества комментариев.
    """
    user_id = get_user_id_by_login(login)
    if user_id is None:
        return {"error": f"User with login '{login}' not found.", "data": []}

    post_ids_with_counts = get_commented_post_ids(user_id)
    post_details = get_post_details(post_ids_with_counts)

    return {"user_login": login, "data": post_details}


if __name__ == "__main__":
    login1 = "user1"
    login2 = "user2"
    print(get_comments_by_login(login1))
    print(get_comments_by_login(login2))
