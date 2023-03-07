from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic


TInput = TypeVar('TInput')


class BaseWriter(
    Generic[TInput],
    metaclass=ABCMeta
):
    """
    Base class for all writers.

    Methods:
        open: Open the writer.
        close: Close the writer.
        write: Write the next item.

    Notes:
        The writer is a context manager. It can be used in a `with` statement.
    """
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    @abstractmethod
    def open(self):
        """
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close the reader.
        """
        pass

    @abstractmethod
    def write(self, item:TInput) -> None:
        """
        Write the next item.
        """
        pass
