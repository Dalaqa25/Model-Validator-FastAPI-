from fastapi import FastAPI, UploadFile, File, HTTPException
from app.routes import router as model_router

app = FastAPI()

# როუტერის/ენდფოინთის დაფიქსირება:
app.include_router(model_router, prefix="/api/models")