# Описание проекта

## Общая информация
Этот проект представляет собой реализацию задания, включающего:
- Создание двух баз данных (SQLite).
- Написание Python-кода для взаимодействия с базами данных.
- Разработку FastAPI-сервера для предоставления данных через API.

---

## Структура проекта
Проект состоит из следующих файлов:

### `comments_data.py`
- Модуль для работы с базой данных `authors_database.db`.
- Содержит функции для получения информации о комментариях пользователя.

### `user_logs.py`
- Модуль для работы с базой данных `logs_database.db`.
- Содержит функции для получения информации о действиях пользователя.

### `server.py`
- FastAPI-сервер, предоставляющий два эндпоинта:
  - `/api/comments` — получение информации о комментариях пользователя.
  - `/api/general` — получение общей информации о действиях пользователя.

### `requirements.txt`
- Список зависимостей для запуска проекта.

### `README.md`
- Описание проекта и инструкции по запуску.

---

## Базы данных

### 1. `authors_database.db`
Содержит следующие таблицы:

#### `users`
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `email` (TEXT, UNIQUE, NOT NULL)
- `login` (TEXT, UNIQUE, NOT NULL)

#### `blog`
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `owner_id` (INTEGER, NOT NULL, FOREIGN KEY REFERENCES users(id))
- `name` (TEXT, NOT NULL)
- `description` (TEXT)

#### `post`
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `header` (TEXT, NOT NULL)
- `text` (TEXT, NOT NULL)
- `author_id` (INTEGER, NOT NULL, FOREIGN KEY REFERENCES users(id))
- `blog_id` (INTEGER, NOT NULL, FOREIGN KEY REFERENCES blog(id))

#### `comment`
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `post_id` (INTEGER, NOT NULL, FOREIGN KEY REFERENCES post(id))
- `user_id` (INTEGER, NOT NULL, FOREIGN KEY REFERENCES users(id))
- `text` (TEXT, NOT NULL)

### 2. `logs_database.db`
Содержит следующие таблицы:

#### `space_type`
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `name` (TEXT, UNIQUE, NOT NULL)

#### `event_type`
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `name` (TEXT, UNIQUE, NOT NULL)

#### `logs`
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `datetime` (TEXT, NOT NULL)
- `user_id` (INTEGER, NOT NULL)
- `space_type_id` (INTEGER, NOT NULL, FOREIGN KEY REFERENCES space_type(id))
- `event_type_id` (INTEGER, NOT NULL, FOREIGN KEY REFERENCES event_type(id))

---

## Что было добавлено

### Таблица `comment`
В базу данных `authors_database.db` была добавлена таблица `comment` для хранения комментариев пользователей к постам.

Поля таблицы:
- `id` — уникальный идентификатор комментария.
- `post_id` — идентификатор поста, к которому оставлен комментарий.
- `user_id` — идентификатор пользователя, оставившего комментарий.
- `text` — текст комментария.

---

## Как запустить проект

### Установка зависимостей
Убедитесь, что у вас установлены все необходимые зависимости. Выполните команду:
```bash
pip install -r requirements.txt
```

### Запуск FastAPI-сервера
Для запуска сервера выполните команду:
```bash
python server.py
```
Сервер будет доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Использование API

### Получение комментариев пользователя
```bash
http://127.0.0.1:8000/api/comments?login=user1
```
**Ответ:**
```json
{
    "user_login": "user1",
    "data": [
        {
            "header": "Post 1",
            "author_login": "author1",
            "comments_count": 1
        },
        {
              "header": "Post 2",
              "author_login": "author2",
              "comments_count": 1
        },
        {
            "header": "Post 3",
            "author_login": "author1",
            "comments_count": 1
        }
    ]
}
```

### Получение общей информации о действиях пользователя
```bash
http://127.0.0.1:8000/api/general?date=2023-10-01
```
**Ответ:**
```json
{
    "date": "2023-10-01",
    "logins": 3,
    "logouts": 1,
    "blog_activity": 2
}
```

---

## Заключение
Все требования задания были выполнены, а также были внесены изменения в структуру баз данных для возможности выполнения задания.


