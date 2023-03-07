from pathlib import Path
from typing import Union, Tuple

import cv2
import numpy as np

from cvflow.io.output.base import BaseWriter


class VideoStreamWriter(BaseWriter):
    """
    Write video to stream.

    Write video to stream. The video is written to a file or device.

    Examples:
        >>> from cvflow.io.output.video import VideoStreamWriter
        >>> with VideoStreamWriter('demos/sample.mp4', fps=30) as output:
        >>>     for index, image in enumerate(images):
        >>>         output.write(image)

    Attributes:
        url_or_device: Path to the video file or device id.
        fps: Frames per second.
        size: Size of the video.
        codec: Codec of the video.
        is_color: Whether the video is color or not.

    Notes:
        Video in this package means that a generator of numpy arrays with shape (H, W, C) and dtype uint8.
        The channel order is RGB.
        This is the same format as PIL.Image and Tensorflow, but different from OpenCV.

    References:
        https://docs.opencv.org/4.5.2/dd/d43/tutorial_py_video_display.html
    """

    def __init__(
            self,
            url_or_device: Union[str, Path, int],
            size: Tuple[int, int],
            *,
            fps: int = 30,
            codec: str = 'mp4v',
            is_color: bool = True,
    ):
        """
        Args:
            url_or_device:
                Path to the video file or device id.

                Examples:
                    - 'demos/sample.mp4'
                    - 0
            fps: Frames per second.
            size: Size of the video.
            codec: Codec of the video.
            is_color: Whether the video is color or not.
        """
        self.url_or_device = url_or_device
        self.fps = fps
        self.size = size
        self.codec = codec
        self.is_color = is_color

        self._writer = None

    def open(self):
        if self._writer is None:
            self._writer = cv2.VideoWriter(
                str(self.url_or_device),
                cv2.VideoWriter_fourcc(*self.codec),
                self.fps,
                self.size,
                self.is_color,
            )
        else:
            raise RuntimeError('VideoWriter is already open.')

    def close(self):
        if self._writer is not None:
            self._writer.release()
            self._writer = None

    def write(self, image: np.ndarray) -> None:
        if self._writer is None:
            self.open()
        self._writer.write(image)


if __name__ == '__main__':
    from cvflow.io.input.video import VideoStreamReader

    with VideoStreamReader('demos/sample.mp4') as reader:
        with VideoStreamWriter('demos/sample_output.mp4', size=(reader.info.width, reader.info.height), codec='mp4v', is_color=True) as writer:
            for index, image in reader:
                writer.write(image)
