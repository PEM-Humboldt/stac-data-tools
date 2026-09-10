from abc import ABC, abstractmethod


class Storage(ABC):
    """
    Abstract storage backend. Each cloud provider is implemented as a
    concrete subclass.
    """

    @abstractmethod
    def upload_file(self, file_name: str, file_path: str) -> str:
        """
        Upload a local file under the key ``file_name`` and return the
        public href that will be stored as the STAC asset href.
        """

    @abstractmethod
    def remove_file(self, file_path: str) -> None:
        """
        Remove an object given the href exactly as it was stored in the
        STAC asset (a full URL) or a bare key.
        """

    @abstractmethod
    def build_object_url(self, file_name: str) -> str:
        """
        Build the public href for a key without uploading anything.
        """
