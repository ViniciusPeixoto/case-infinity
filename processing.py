import cv2
from scipy.spatial import distance

from models import Image

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256


class ImageProcessor:
    """
    The ImageProcessor holds all processing done to the image in the
    context of the project.
    """

    images: dict = dict()

    def load_image(self, image: Image) -> None:
        """
        Loads an Image to the ImageProcessor.
        The path to the image becomes its access key.
        Maximum of two loaded images at a time.

        Args:
        - image: an instance of Image.

        Raises:
        - ValueError: if OpenCV cannot read the image file.
        - ValueError: if tries to load more than 2 images.
        """
        if len(self.images) < 2:
            loaded = cv2.imread(image.path)
            if loaded is None:
                raise ValueError(f'{image.path}: Could not load image.')
            self.images[image.path] = loaded
        else:
            raise ValueError('ImageProcessor already at maximum capacity')

    def to_grayscale(self):
        """
        Converts all loaded images to grayscale.
        """
        for image in self.images:
            target = self.images[image]
            if len(target.shape) == 2:
                # A grayscale image should not be converted to grayscale
                continue
            self.images[image] = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        return self

    def rescale(self):
        """
        Resizes all loaded images to designated sizes.
        """
        for image in self.images:
            self.images[image] = cv2.resize(
                self.images[image],
                (IMAGE_WIDTH, IMAGE_HEIGHT),
            )

        return self

    def get_histogram(self, key: str):
        """
        Generates the histogram for a loaded images.

        Args:
        - key: the key to access the image in the dictionary.

        Raises:
        - ValueError: if the loaded image is not in grayscale.
        """
        if not len(self.images[key].shape) == 2:
            raise ValueError('Image is not in grayscale.')

        return cv2.calcHist(
            [self.images[key]],
            [0],  # grayscale channel
            None,  # no mask used
            [256],  # 256 bins
            [0, 256],  # range of pixel values
        )

    def get_cosine_distance(self):
        """
        Calculates the cosine distance between the two loaded images.

        Raises:
        - ValueError: if a loaded image is not in grayscale.
        """
        if any(
            [len(image.shape) != 2 for image in list(self.images.values())]
        ):
            raise ValueError('Image is not in grayscale.')

        histograms = (
            self.get_histogram(image).flatten() for image in self.images
        )

        return distance.cosine(*histograms)

    def concatenate_images(self, dst):
        """
        Concatenate horizontally all loaded images.

        Args:
        - dst: the destination path where the new image file will be saved.
        """
        cv2.imwrite(dst, cv2.hconcat(list(self.images.values())))


processor = ImageProcessor()
