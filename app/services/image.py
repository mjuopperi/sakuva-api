from PIL.Image import Image as PILImage


IMAGE_MAX_DIMENSION = 2000


def get_resize_factor(image: PILImage) -> float:
    """
    Returns a value between 0 and 1 that can be used to resize the image so that its highest dimension is IMAGE_MAX_DIMENSION

    e.g. 4321 x 1800 image would return factor = IMAGE_MAX_DIMENSION / 4321
         -> factor * 4321 = 2000 and factor * 1800 < 2000
    """
    highest_dimension = max(image.width, image.height)
    if highest_dimension > IMAGE_MAX_DIMENSION:
        return IMAGE_MAX_DIMENSION / highest_dimension
    return 1


def resize(image: PILImage) -> PILImage:
    resize_factor = get_resize_factor(image)
    return image.resize((int(image.width * resize_factor), int(image.height * resize_factor)))


def save_optimized(image: PILImage, image_path: str):
    image.save(image_path, optimize=True, quality=80, progressive=True, dpi=(300, 300))


def create_thumbnail(image: PILImage, width: int, image_dir: str, filename: str):
    """
    Creates a thumbnail of given width of the image and saves it with _<width> appended to filename.

    e.g. /img/47/29/104729.jpg -> /img/47/29/104729_500.jpg
    """
    height = (image.height * width) // image.width
    file_id, file_extension = filename.split(".")
    thumbnail_path = f"{image_dir}/{file_id}_{width}.{file_extension}"

    thumbnail = image.resize((width, height))
    thumbnail.save(thumbnail_path, progressive=True, dpi=(300, 300))
