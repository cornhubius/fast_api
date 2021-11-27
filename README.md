# fast_api

HOW TO USE

1. Clone repo `git clone https://github.com/cornhubius/fast_api`
2. `cd fast_api/`
3. We use pipenv. Install it: `pip install pipenv`
4. If not activated automatically, activate env: `pipenv shell`
5. Install dependenses: `pipenv install Pipfile`
6. Create .env file:`touch .env && echo "DATABASE_URL=<your database url>" > .env`
7. Apply to alembic migrations: `alembic upgrade head`
8. Run app: `python main.py`
9. Available at: `localhost:8000/`


DOCKER
1. Run: `docker-compose up --build`
2. Available at: `localhost:5000/`

TEST
1.Run: `pytest`

DOCS API
1. Available at: `localhost:8000/docs`


