import os

from fastapi import APIRouter, UploadFile, HTTPException, Depends
from psycopg.rows import class_row

from app.config import Settings
from app.dependencies import verify_api_key
from app.models import ImageIn, ImageOut
from app.services.db import db

settings = Settings()
router = APIRouter(prefix="/api")

BASE_IMG_PATH = f"{settings.media_dir}/img"


def filename_to_path(filename: str) -> str:
    """
    Creates a path with two subdirectories for a given filename.

    e.g. "104729.jpg" -> "47/29/104729.jpg"
    """
    file_id, extension = filename.split(".")
    if len(file_id) < 4:
        return f"{BASE_IMG_PATH}/x/{file_id}/{filename}"
    dir1 = file_id[-4:-2]
    dir2 = file_id[-2:]
    return f"{BASE_IMG_PATH}/{dir1}/{dir2}/{filename}"


def file_path_to_url_path(file_path: str) -> str:
    """
    Returns url path of image.

    e.g. /media/img/47/29/104729.jpg -> /img/47/29/104729.jpg
    """
    image_path = "/".join(file_path.split("/")[-4:])
    return f"/{image_path}"


@router.post("/image", status_code=201, dependencies=[Depends(verify_api_key)])
async def post_image(image_file: UploadFile):
    file_path = filename_to_path(image_file.filename)
    print(file_path)
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            while contents := image_file.file.read(1024 * 1024):
                f.write(contents)
        return "ok"
    except Exception as e:
        print(f"There was an error uploading the file:\n{e}")
        raise HTTPException(status_code=500, detail="There was an error uploading the file")
    finally:
        await image_file.close()


@router.post("/image/meta", status_code=201, dependencies=[Depends(verify_api_key)])
def post_image_meta(image: ImageIn):
    image_file_path = filename_to_path(f"{image.id}.{image.file_extension}")
    if not os.path.isfile(image_file_path):
        raise HTTPException(404, detail="Image not found. Save image before metadata.")

    with db.cursor() as cursor:
        stmt = """
            insert into image (id, doc_id, photographer, caption, description, location, date, url_path)
            values (%(id)s, %(doc_id)s, %(photographer)s, %(caption)s, %(description)s, %(location)s, %(date)s, %(url_path)s)
            on conflict (id) do update
            set 
                doc_id = excluded.doc_id, 
                photographer = excluded.photographer, 
                caption = excluded.caption, 
                description = excluded.description,
                location = excluded.location,
                date = excluded.date,
                url_path = excluded.url_path
        """
        cursor.execute(stmt, {**image.dict(), "url_path": file_path_to_url_path(image_file_path)})
        return "ok"


@router.get("/image/meta/{image_id}", response_model=ImageOut)
def get_image_meta(image_id: int):
    with db.cursor(row_factory=class_row(ImageOut)) as cursor:
        cursor.execute("select * from image where id = %s", (image_id,))
        res = cursor.fetchone()
        if not res:
            raise HTTPException(404, detail="Not found")
        return res
