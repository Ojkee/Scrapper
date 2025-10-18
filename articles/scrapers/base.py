from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar


T = TypeVar("T")


class SoupParser(ABC, Generic[T]):
    @abstractmethod
    def parse(self, soup) -> Optional[T]:
        pass
