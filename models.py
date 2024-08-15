import imghdr
import os

from pydantic import BaseModel, field_validator


class Setup(BaseModel):
    image_a: str
    image_b: str
    output_location: str
    threshold: float


class Image(BaseModel):
    path: str

    @field_validator('path', mode='before')
    def validate_path(cls, value):
        absolute_path = os.path.abspath(value)

        if not os.path.isfile(absolute_path):
            raise ValueError(f'{absolute_path}: This file does not exist.')

        if not imghdr.what(absolute_path) == 'jpeg':
            raise ValueError(f'{absolute_path} is not a valid JPG image.')

        return absolute_path
