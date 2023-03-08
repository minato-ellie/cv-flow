from pathlib import Path
from typing import overload, Union, Iterator

import numpy as np

from cvflow.io.input import VideoDeviceReader, VideoFileReader, VideoUrlReader, VideoStreamReader
from cvflow.runner.base import BaseRunner


class VideoStreamRunner(
    BaseRunner[np.ndarray]
):
    @overload
    def __init__(
            self,
            url_or_device: Union[str, Path, int],
            num_frames: int = None,
            num_retries: int = 0,
            wait_time: int = 0.025,
            *,
            fps: float = None,
    ):
        ...

    @overload
    def __init__(
            self,
            reader: VideoStreamReader,
            *,
            fps: float = None,
    ):
        ...

    def __init__(self, *args, **kwargs):
        fps = kwargs.pop('fps', None)
        super().__init__(fps=fps)

        if len(args) == 1 and isinstance(args[0], VideoStreamReader) and len(kwargs) == 0:
            self._reader = args[0]
        elif 'reader' in kwargs and len(args) == 0 and kwargs.keys() == {'reader'}:
            self._reader = kwargs['reader']
        else:
            self._reader = VideoStreamReader(*args, **kwargs)

        assert isinstance(self._reader, VideoStreamReader), 'reader must be VideoStreamReader'
        self.info = self._reader.info

    def generate(self) -> Iterator[np.ndarray]:
        for frame in self._reader:
            yield frame


class VideoFileRunner(
    VideoStreamRunner
):
    @overload
    def __init__(
            self,
            video_file: Union[str, Path],
            num_frames: int = None,
    ):
        ...

    @overload
    def __init__(
            self,
            reader: VideoFileReader
    ):
        ...

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], VideoFileReader):
            reader = args[0]
        elif 'reader' in kwargs and len(args) == 0 and kwargs.keys() == {'reader'}:
            reader = kwargs['reader']
        else:
            reader = VideoFileReader(*args, **kwargs)
        fps = kwargs.pop('fps', None)

        super().__init__(reader=reader, fps=fps)


class VideoUrlRunner(
    VideoStreamRunner
):
    @overload
    def __init__(
            self,
            url: str,
            num_frames: int = None,
            num_retries: int = 0,
            wait_time: int = 0.025,
    ):
        ...

    @overload
    def __init__(
            self,
            reader: VideoUrlReader
    ):
        ...

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], VideoUrlReader):
            reader = args[0]
        elif 'reader' in kwargs and len(args) == 0 and kwargs.keys() == {'reader'}:
            reader = kwargs['reader']
        else:
            reader = VideoUrlReader(*args, **kwargs)
        fps = kwargs.pop('fps', None)

        super().__init__(reader=reader, fps=fps)


class VideoDeviceRunner(
    VideoStreamRunner
):
    @overload
    def __init__(
            self,
            device: int,
            fps: int = 30,
            *,
            num_frames: int = None,
            num_retries: int = 0,
            wait_time: int = 0.025,
    ):
        ...

    @overload
    def __init__(
            self,
            reader: VideoDeviceReader,
            fps: int = 30,
    ):
        ...

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], VideoDeviceReader):
            reader = args[0]
        elif 'reader' in kwargs and len(args) == 0 and kwargs.keys() == {'reader'}:
            reader = kwargs['reader']
        else:
            reader = VideoDeviceReader(*args, **kwargs)
        fps = kwargs.pop('fps', None)

        super().__init__(reader=reader, fps=fps)
