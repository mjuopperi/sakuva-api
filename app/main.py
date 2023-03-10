import uvicorn
from fastapi import FastAPI

from app import routes

app = FastAPI(title="SA-kuva API")

app.include_router(routes.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
