import pytest
from PIL import Image

from cvflow.io.input.image import *


def test_image_reader():
    reader = ImageReader('demos/sample.jpg')
    assert reader.next().shape == (3264, 4896, 3)
    reader.close()

    with ImageReader('demos/sample.jpg') as reader:
        assert reader.next().shape == (3264, 4896, 3)


def test_image_reader_correct():
    ref_image = np.array(Image.open('demos/sample.jpg'))

    reader = ImageReader('demos/sample.jpg')
    image = reader.next()
    reader.close()

    assert np.all(image == ref_image)

    with ImageReader('demos/sample.jpg') as reader:
        image = reader.next()
        assert np.all(image == ref_image)


def test_image_channel(tmp_path):
    """
    Test if the image reader can read the correct channel order

    Write a test image which has pure
    red in the first row,
    pure green in the second row,
    and pure blue in the third row.
    """

    image = np.zeros((3, 3, 3), dtype=np.uint8)
    image[0, :, 0] = 255
    image[1, :, 1] = 255
    image[2, :, 2] = 255
    Image.fromarray(image).save(str(tmp_path / 'test.png'))

    # Read the image and check the channel order
    reader = ImageReader(str(tmp_path / 'test.png'))
    image = reader.next()
    reader.close()
    assert np.all(image[0, :] == [255, 0, 0], axis=-1).all() # noqa E712
    assert np.all(image[1, :] == [0, 255, 0], axis=-1).all()
    assert np.all(image[2, :] == [0, 0, 255], axis=-1).all()

    # Read the image and check the channel order
    with ImageReader(str(tmp_path / 'test.png')) as reader:
        image = reader.next()
        assert np.all(image[0, :] == [255, 0, 0], axis=-1).all() # noqa E712
        assert np.all(image[1, :] == [0, 255, 0], axis=-1).all()
        assert np.all(image[2, :] == [0, 0, 255], axis=-1).all()


