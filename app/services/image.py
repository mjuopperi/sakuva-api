from PIL.Image import Image as PILImage


def create_thumbnail(image: PILImage, width: int, image_dir: str, filename: str):
    """
    Creates a thumbnail of given width of the image and saves it with _<width> appended to filename.

    e.g. /img/47/29/104729.jpg -> /img/47/29/104729_500.jpg
    """
    height = (image.height * width) // image.width
    file_id, file_extension = filename.split(".")
    thumbnail_path = f"{image_dir}/{file_id}_{width}.{file_extension}"

    thumbnail = image.copy()
    thumbnail.thumbnail((width, height))
    thumbnail.save(thumbnail_path)
