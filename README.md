# HOW TO USE
1. [RUN_IN_DOCKER](#RUN_IN_DOCKER)
2. [RUN IN LOCAL MACHINE](#RUN_IN_LOCAL_MACHINE)
3. [TEST](#TEST)
4. [DOCS_API](#DOCS_API)

## RUN IN DOCKER: <a name="RUN_IN_DOCKER"></a>
1. Clone repo
```bash
git clone https://github.com/cornhubius/fast_api
```
2. Open `fast_api` directory
```bash
cd fast_api/
```
3. Run: 
```bash
docker-compose up --build
```
4. Available at: 
```bash 
localhost:5000/
```


## RUN IN LOCAL MACHINE: <a name="RUN_IN_LOCAL_MACHINE"></a>
1. Clone repo
```bash
git clone https://github.com/cornhubius/fast_api
```
2. Open `fast_api` directory
```bash
cd fast_api/
```
3. We use pipenv. Install it: 
```bash
pip install pipenv
```
4. If not activated automatically, activate env: 
```bash
pipenv shell
```
5. Install dependenses: 
```bash
pipenv install Pipfile
```
6. Create .env file:
```bash
touch .env && echo "DATABASE_URL=<your database url>" > .env
```
7. Apply to alembic migrations: 
```bash
alembic upgrade head
```
8. Run app: 
```bash
python main.py
```
9. Available at: 
```bash
localhost:8000/
```


## TEST: <a name="TEST"></a>
Run: 
```bash 
pytest
```


# DOCS API: <a name="DOCS_API"></a>
1. Run app
2. Docs available at: 
```bash
localhost:8000/docs
```


