from abc import ABC, abstractmethod
from shared.logger import get_logger


class BaseConnector(ABC):

    def __init__(self, config):
        self.config = config
        self.source_name = config.get("source_name", config.get("name", "unknown"))
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def read(self):
        """Read data from the source."""
        pass