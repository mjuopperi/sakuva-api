from datetime import date as date_type

from pydantic import BaseModel as PydanticBaseModel, Field
from pydantic.utils import to_lower_camel


class BaseModel(PydanticBaseModel):
    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class Image(BaseModel):
    id: int = Field(description="Id of the image", example=1337)
    photographer: str = Field(
        "Tuntematon", description="Photographer", example="Heikki Roivanen, Auvo Mustonen, Sulo Tammilehto"
    )
    caption: str = Field("", description="Media caption")
    description: str = Field("", description="Media description")
    location: str = Field(description="Name of location where photo was taken", example="Rovaniemi")
    date: date_type | None = Field(None, description="Date when image was taken", example=date_type(1939, 11, 30))


class ImageIn(Image):
    file_extension: str = Field(description="File extension", example="jpg")


class ImageOut(Image):
    url_path: str = Field(description="URL path to image file", example="/img/12/39/1331239.jpg")
