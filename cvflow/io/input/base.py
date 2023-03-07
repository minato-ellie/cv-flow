from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

TOutput = TypeVar('TOutput')


class BaseReader(
    Generic[TOutput],
    metaclass=ABCMeta
):
    """
    Base class for all readers.

    Methods:
        open: Open the reader.
        close: Close the reader.
        next: Read next value.

    Notes:
        The Reader is a context manager. It can be used in a `with` statement.
    """
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.next()
        if item is None:
            raise StopIteration
        return item

    def __del__(self):
        self.close()

    @abstractmethod
    def open(self):
        """
        Open the reader.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close the reader.
        """
        pass

    @abstractmethod
    def next(self) -> TOutput:
        """
        Read the next item.
        """
        pass
