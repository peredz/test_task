import uvicorn
from fastapi import FastAPI
from comments_data import get_comments_by_login
from user_logs import get_user_activity_by_date

app = FastAPI()


@app.get("/api/comments")
def get_comments(login: str):
    """
    Эндпоинт для получения информации о комментариях пользователя.
    """
    result = get_comments_by_login(login)
    return result


@app.get("/api/general")
def get_general(date: str):
    """
    Эндпоинт для получения общей информации о действиях пользователя.
    """
    result = get_user_activity_by_date(date)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
