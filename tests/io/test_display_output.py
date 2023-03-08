import pytest

from cvflow.io.output.display import *


def test_display_writer():
    writer = DisplayWriter()
    writer.write(np.zeros((4, 4, 3), dtype=np.uint8))
    writer.close()

    with DisplayWriter() as writer:
        writer.write(np.zeros((4, 4, 3), dtype=np.uint8))

    with pytest.raises(RuntimeError):
        writer.close()


def test_display_writer_loop():
    import cv2
    with DisplayWriter() as writer:
        for _ in range(10):
            input = np.random.randint(0, 255, (4, 4, 3), dtype=np.uint8)
            writer.write(input)
