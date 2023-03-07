import time
from pathlib import Path
from typing import Union, Tuple
from collections import namedtuple

import cv2
import numpy as np

from cvflow.io.input.base import BaseReader


VideoInfo = namedtuple('VideoInfo', ['fps', 'width', 'height', 'num_frames'])


class VideoStreamReader(BaseReader):
    """
    Read video from stream.

    Read video from stream, such as a file or a camera. This class is a wrapper of cv2.VideoCapture.

    Examples:
        >>> from cvflow.io.input.video import VideoStreamReader
        >>> for index, image in VideoStreamReader('demos/sample.mp4'):
        >>>     print(image.shape)
        (720, 1280, 3)
        ...
        >>> with VideoStreamReader('demos/sample.mp4') as input:
        >>>     for index, image in input:
        >>>         print(f'Frame {index}: {image.shape}')
        Frame 1: (720, 1280, 3)
        Frame 2: (720, 1280, 3)
        ...

    Attributes:
        url_or_device: Path to the video file or device id.

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
            num_frames: int = None,
            num_retries: int = 0,
            wait_time: int = 0.025,
    ):
        """
        Args:
            url_or_device:
                Path to the video file or device id.

                Examples:
                    - 'demos/sample.mp4'
                    - 0
                    - 'https://mazwai.com/videvo_files/video/free/2018-12/small_watermarked/180607_A_124_preview.mp4'
        num_frames: Number of frames to read. If None, read all frames.
        num_retries: Number of retries to read the video. Default is 0, which means no retry.
        wait_time: Time to wait before retrying, in seconds. Default is 0.025.
        """
        if isinstance(url_or_device, Path):
            url_or_device = str(url_or_device)
        if not isinstance(url_or_device, (str, int)):
            raise TypeError(f'Expected url_or_device to be str or int, got {type(url_or_device)}')

        if num_frames is not None and num_frames <= 0:
            raise ValueError(f'Expected num_frames to be positive, got {num_frames}')
        if num_retries < 0:
            raise ValueError(f'Expected num_retries to be non-negative, got {num_retries}')

        self.url_or_device = url_or_device
        self._video = None
        self._num_frames = num_frames
        self._frame_count = 0
        self._num_retries = num_retries
        self._retries_count = 0
        self.wait_time = wait_time
        super(VideoStreamReader, self).__init__()

    def open(self):
        """
        Open the video.
        """
        if self._video is None:
            self._video = cv2.VideoCapture(self.url_or_device)

    @property
    def info(self) -> VideoInfo:
        """
        Get video info.

        Returns:
            A dict of video info.
        """
        if self._video is None:
            self.open()

        if self._video.isOpened():
            return VideoInfo(
                fps=int(self._video.get(cv2.CAP_PROP_FPS)),
                width=int(self._video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                height=int(self._video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                num_frames=int(self._video.get(cv2.CAP_PROP_FRAME_COUNT)),
            )
        else:
            raise RuntimeError('Video is not opened')

    def close(self):
        """
        Close the video.
        """
        if self._video and self._video.isOpened():
            self._video.release()

    def next(self) -> Tuple[int, np.ndarray]:
        """
        Read the next frame.
        Returns:
            A tuple of frame count and frame. Frame count starts from 1.

            Notes:
                Frame is a numpy array with shape (H, W, C) and dtype uint8.
                The channel order is RGB.
                **This is the same format as PIL.Image and Tensorflow, but different from OpenCV**.
        """
        if self._video is None:
            self.open()

        if self._video.isOpened():
            ret, frame = self._video.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self._frame_count += 1
                if self._num_frames and self._frame_count >= self._num_frames:
                    self.close()
                    raise StopIteration
                return self._frame_count, frame
            else:
                if self._num_retries and self._retries_count < self._num_retries:
                    self._retries_count += 1
                    time.sleep(self.wait_time)
                    return self.next()
                else:
                    self.close()
                    raise StopIteration
        else:
            raise StopIteration


class VideoUrlReader(VideoStreamReader):
    """
    Read video from url.

    Examples:
        >>> from cvflow.io.input.video import VideoUrlReader
        >>> for image in VideoUrlReader('https://mazwai.com/videvo_files/video/free/2018-12/small_watermarked/180607_A_124_preview.mp4'):
        >>>     print(image.shape)
        (720, 1280, 3)
    """ # noqa E501
    def __init__(self, url: str, num_frames: int = None, num_retries=0, wait_time=0.025):
        """

        Args:
            url: url to the video.
            num_frames: Number of frames to read. If None, read until device is closed.
            num_retries: Number of retries to read the video.
            wait_time: Time to wait before retry.
        """
        super(VideoUrlReader, self).__init__(url, num_frames=num_frames, num_retries=num_retries, wait_time=wait_time)


class VideoDeviceReader(VideoStreamReader):
    """
    Read video from device.

    Examples:
        >>> from cvflow.io.input.video import VideoDeviceReader
        >>> for image in VideoDeviceReader(0):
        >>>     print(image.shape)
        (720, 1280, 3)
    """
    def __init__(self, device_id: int = 0, num_frames: int = None, num_retries=0, wait_time=0.025):
        """
        Args:
            device_id:
                Device id. If device_id is 0, it will read from the first camera.
            num_frames: Number of frames to read. If None, read until device is closed.
            num_retries: Number of retries to read the video.
            wait_time: Time to wait before retry.
        """
        super(VideoDeviceReader, self).__init__(device_id, num_frames=num_frames, num_retries=num_retries, wait_time=wait_time)


class VideoFileReader(VideoStreamReader):
    """
    Read video from file.

    Examples:
        >>> from cvflow.io.input.video import VideoFileReader
        >>> for image in VideoFileReader('demos/sample.mp4'):
        >>>     print(image.shape)
        (720, 1280, 3)

    Notes:
        retry is not supported for VideoFileReader.
    """
    def __init__(self, video_file: Union[str, Path], num_frames=None):
        """
        Args:
            video_file: Path to the video file.
            num_frames: Number of frames to read.
        """
        super(VideoFileReader, self).__init__(
            video_file,
            num_frames=num_frames,
            num_retries=0
        )
