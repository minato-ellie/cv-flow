import multiprocessing
import uuid
from typing import Tuple

import cv2
import numpy as np

from cvflow.io.output.base import BaseWriter


class DisplayWriter(BaseWriter[np.ndarray], multiprocessing.Process):

    def __init__(
            self,
            name: str = None,
            size: Tuple[int, int] = None,
            fps: int = 30,
            **kwargs
    ):
        super(DisplayWriter, self).__init__()
        multiprocessing.Process.__init__(self)
        self.name = name or f'cvflow-display-{uuid.uuid4()}'
        self.size = size
        self._wait_time = int(1000 / fps)
        self.kwargs = kwargs

        self._out_pipe, self._in_pipe = multiprocessing.Pipe()
        self._process = None
        self._window = None
        self._is_open = False
        self._is_close = False

    @property
    def fps(self):
        return 1000. / float(self._wait_time)

    @fps.setter
    def fps(self, value):
        self._wait_time = int(1000 / value)

    def open(self):
        if self._is_open:
            return
        self._process = multiprocessing.Process(target=self._run)
        self._process.start()
        self._is_open = True

    def close(self):
        if self._is_close:
            return
        self._out_pipe.send(None)
        self._is_close = True

    def write(self, item: np.ndarray):
        self._out_pipe.send(item)

    def run(self):
        window_name = self.name
        wait_time = self._wait_time

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        if self.size is not None:
            cv2.resizeWindow(window_name, *self.size)

        while True:
            try:
                item = self._in_pipe.recv()

                if item is None:
                    break
                cv2.imshow(window_name, item)
            except EOFError:
                break
            cv2.waitKey(wait_time)

        cv2.destroyWindow(window_name)

    def __del__(self):
        self.close()
