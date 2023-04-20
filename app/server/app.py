from fastapi import FastAPI
from server.routes.student import router as StudentRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")

@app.get("/", tags=["Root"])
async def root():
    return {"message": "welcome!!"}