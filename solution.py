import argparse
import sys

import yaml
from pydantic import ValidationError

from models import Image, Setup
from processing import processor

parser = argparse.ArgumentParser(description='Check for image similarity')
parser.add_argument(
    '-y',
    '--yaml',
    type=argparse.FileType(),
    help='YAML file with execution settings.',
    required=True,
)


def main(first: Image, second: Image, setup: Setup):
    try:
        processor.load_image(first)
        processor.load_image(second)
    except ValueError as err:
        print(f'Error loading the images: {err}')
        return

    # Apply image processing
    processor.to_grayscale().rescale()

    try:
        distance = processor.get_cosine_distance()
    except ValueError as err:
        print(f'Error calculating cosine distance: {err}')
        return

    print(f'Distance: {distance}')
    print(
        f'{"Same product." if distance < setup.threshold else "Different products."}'
    )
    processor.concatenate_images(setup.output_location)


if __name__ == '__main__':
    args = parser.parse_args()
    try:
        settings = yaml.load(args.yaml, Loader=yaml.CLoader)
    except Exception as err:
        print(f'Error loading the settings from YAML: {err}')
        sys.exit()

    try:
        setup = Setup(**settings)
    except ValidationError as err:
        print(f'Invalid settings from YAML: {err}')
        sys.exit()

    try:
        first = Image(path=setup.image_a)
        second = Image(path=setup.image_b)
    except ValidationError as err:
        print(f'Error loading the images: {err}')
        sys.exit()

    main(first, second, setup)
