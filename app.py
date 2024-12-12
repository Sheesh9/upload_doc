from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import shutil
import os

from database import SessionLocal, engine
from models import Document, init_db

app = FastAPI()

# Инициализация базы данных
init_db()


# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload_doc/")
async def upload_doc(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Проверка расширения файла (например, только изображения)
    if not file.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Сохранение файла на диск в папку documents/
    file_location = f"documents/{file.filename}"

    # Создаем папку documents, если она не существует
    os.makedirs("documents", exist_ok=True)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Добавление записи в базу данных
    db_document = Document(filename=file.filename, filepath=file_location)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return JSONResponse(content={"filename": db_document.filename, "filepath": db_document.filepath})