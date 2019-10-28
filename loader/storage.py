import os
from abc import ABC, abstractmethod


class Storage(ABC):
    """
    Class storage is an abstract class for any kind of storage. Its purpose is to define the Storage interface.
    """
    @abstractmethod
    def store(self, name: str, content) -> None:
        """
        store stores the given content under the given name.
        """


class RamStorage(Storage):
    def __init__(self):
        self._storage = dict()

    def store(self, name: str, content) -> None:
        if name == "":
            raise Exception("empty name")
        self._storage[name] = content


class FileStorage(Storage):
    def __init__(self, directory):
        self.target_dir = directory

    def store(self, name: str, content) -> None:
        with open(os.path.join(self.target_dir, name), "wb") as f:
            f.write(content)
