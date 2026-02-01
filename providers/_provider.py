import asyncio
from abc import ABC, abstractmethod
import logging

from classes.application_result import ApplicationResult

logger = logging.getLogger("flat-apply")

class Provider(ABC):
    @property
    @abstractmethod
    def domain(self) -> str:
        """every flat provider needs a domain"""
        pass

    @abstractmethod
    async def apply_for_flat(self, url: str) -> ApplicationResult:
        pass

    def test_apply(self, url):
        print(asyncio.run(self.apply_for_flat(url)))
