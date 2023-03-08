import time
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Callable, Iterator

from cvflow.utils.runner import AsyncRunner, ThreadRunner

TInput = TypeVar('TInput')


class BaseRunner(
    Generic[TInput],
    metaclass=ABCMeta
):
    """
    Base class for all runners.

    Methods:
        run: Run the runner.

    Notes:
        The runner is a context manager. It can be used in a `with` statement.
    """

    def __init__(self, fps: float = None):
        self.wait_time = 1. / fps if fps is not None else 0.

    @property
    def fps(self) -> float:
        return 1. / self.wait_time

    @fps.setter
    def fps(self, value: float):
        self.wait_time = 1. / value

    @abstractmethod
    def generate(self) -> Iterator[TInput]:
        """
        Generate the next item.
        """
        pass

    def run(self, func: Callable[[TInput], None]) -> None:
        """
        Run the runner.
        """
        runner = ThreadRunner.create()
        for item in self.generate():
            start = time.perf_counter()
            runner.forward(func, item)
            end = time.perf_counter()

            if self.wait_time - (end - start) > 0:
                time.sleep(self.wait_time - (end - start))

    def run_async(self, func) -> None:
        """
        Run the runner asynchronously.
        """
        runner = AsyncRunner.create()
        for item in self.generate():
            runner.forward(func, item)
            time.sleep(self.wait_time)
