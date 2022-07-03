from fastapi import FastAPI
import uvicorn
from app.endpoints import jokes, maths

app = FastAPI()

app.include_router(jokes.router)
app.include_router(maths.router)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # 127.0.0.1:8000/docs para acceder a la documentación
