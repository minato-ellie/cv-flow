from pathlib import Path
from typing import Union, Iterable

import cv2
import numpy as np

from cvflow.io.input.base import BaseReader


def read_image(image: Union[str, Path]) -> np.ndarray:
    """
    Reads an image from the given path

    Args:
        image: Path to the image

    Returns:
        Image as a numpy array. (H, W, C) and dtype uint8, Channel order is RGB.
    """
    return cv2.cvtColor(cv2.imread(str(image)), cv2.COLOR_BGR2RGB)


class ImageReader(BaseReader[np.ndarray]):
    """
    Base class for image readers

    Args:
        images: Iterable of paths to images

    Raises:
        NotImplementedError: If the class is not implemented

    Examples:
        >>> from cvflow.io.input.image import ImageFolderReader
        >>> reader = ImageFolderReader('path/to/folder')
        >>> reader.open()
        >>> for image in reader:
        >>>     print(image.shape)
        (H, W, C)
        >>> reader.close()

        >>> from cvflow.io.input.image import ImageFolderReader
        >>> reader = ImageFolderReader('path/to/folder')
        >>> with reader:
        >>>     for image in reader:
        >>>         print(image.shape)
        (H, W, C)
    """
    def __init__(self, images: Union[Iterable[Union[str, Path]], str, Path]):
        """

        Args:
            images: Iterable of paths to images
        """
        if isinstance(images, (str, Path)):
            images = [images, ]

        self._images = [str(image) for image in images]
        self._image_cache = None

    def open(self):
        self._image_cache = [read_image(image) for image in self._images]

    def close(self):
        self._image_cache = None

    def next(self) -> np.ndarray:
        """
        Read the next image
        Returns:
            Image as a numpy array. (H, W, C) and dtype uint8, Channel order is RGB.
        """
        if self._image_cache is None:
            self.open()

        if not self._image_cache:
            raise StopIteration
        return self._image_cache.pop(0)


class ImageFolderReader(ImageReader):
    """
    Read images from a folder
    """
    def __init__(self, folder: Union[str, Path], pattern: str = "*"):
        """
        Args:
            folder: Path to the folder
            pattern: Pattern to match the images. Default is "*"
        """
        super().__init__(Path(folder).glob(pattern))


class VideoFolderReader(ImageReader):
    """
    Read Sequence of images from a folder

    Warnings:
        This class is not implemented yet.
    """
    def __init__(self, folder: Union[str, Path], images: Iterable[Union[str, Path]], pattern: str = "*"):
        """
        Args:
            folder: Path to the folder
            pattern: Pattern to match the images. Default is "*"
        """
        super().__init__(images)
        raise NotImplementedError
