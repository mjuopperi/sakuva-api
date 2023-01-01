from app.config import get_settings

settings = get_settings()

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
