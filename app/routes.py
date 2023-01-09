import io
import os
from datetime import date
from typing import List

from fastapi import APIRouter, UploadFile, HTTPException, Depends, BackgroundTasks
from psycopg.rows import class_row
import PIL.Image

from app.config import get_settings
from app.dependencies import verify_api_key
from app.models import ImageIn, ImageOut
from app.services.db import db
from app.services.es import es
from app.services.image import create_thumbnail, resize, save_optimized
from app.util import filename_to_path

settings = get_settings()
router = APIRouter(prefix="/api")


@router.post("/image", status_code=201, dependencies=[Depends(verify_api_key)])
async def post_image(image_file: UploadFile, background_tasks: BackgroundTasks):
    file_path = filename_to_path(image_file.filename)
    try:
        image_dir = os.path.dirname(file_path)
        os.makedirs(image_dir, exist_ok=True)

        request_object_content = await image_file.read()
        image = PIL.Image.open(io.BytesIO(request_object_content))
        resized = resize(image)
        save_optimized(resized, file_path)

        for size in settings.thumbnail_sizes:
            background_tasks.add_task(create_thumbnail, resized, size, image_dir, image_file.filename)

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

    image_out = image.to_image_out()

    with db.cursor() as cursor:
        stmt = """
            insert into image (id, photographer, caption, description, location, date, url_path, width, height, is_color, is_placeholder)
            values (%(id)s, %(photographer)s, %(caption)s, %(description)s, %(location)s, %(date)s, %(url_path)s, %(width)s, %(height)s, %(is_color)s, %(is_placeholder)s)
            on conflict (id) do update
            set 
                photographer = excluded.photographer, 
                caption = excluded.caption, 
                description = excluded.description,
                location = excluded.location,
                date = excluded.date,
                url_path = excluded.url_path,
                width = excluded.width,
                height = excluded.height,
                is_color = excluded.is_color,
                is_placeholder = excluded.is_placeholder
        """
        cursor.execute(stmt, image_out.dict())
        es.index(image_out)
        return "ok"


@router.get("/image/meta/{image_id}", response_model=ImageOut)
def get_image_meta(image_id: int):
    with db.cursor(row_factory=class_row(ImageOut)) as cursor:
        cursor.execute("select * from image where id = %s", (image_id,))
        res = cursor.fetchone()
        if not res:
            raise HTTPException(404, detail="Not found")
        return res


@router.get("/image/search", response_model=List[ImageOut])
def search(q: str | None = "", start: date | None = None, end: date | None = None, color: bool | None = None):
    query = {
        "bool": {
            "must": list(
                filter(
                    None,
                    [
                        es.multi_match(q),
                    ],
                )
            ),
            "filter": list(
                filter(
                    None,
                    [
                        es.date_filter("date", start, end),
                        es.bool_filter("is_color", color),
                        es.bool_filter("is_placeholder", False),
                    ],
                )
            ),
        }
    }
    return es.search(query, ImageOut)


@router.post("/image/reindex", dependencies=[Depends(verify_api_key)])
def reindex(ids: List[int]):
    with db.cursor(row_factory=class_row(ImageOut)) as cursor:
        cursor.execute("select * from image where id = any(%s)", [ids])
        images = cursor.fetchall()
        for image in images:
            es.index(image)
        return "ok"
