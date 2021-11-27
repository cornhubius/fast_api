import uvicorn
from fastapi import FastAPI

from db.base import database
from routes import auth, user, users_list

app = FastAPI()
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users_list.router, prefix="/user-list", tags=["user-list"])


@app.get("/")
def index():
    return {'Hello world!'}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
