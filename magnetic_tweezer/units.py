from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Unit(ABC):
    quantity: float

    @abstractmethod
    def to(self, other_unit: str) -> float:
        pass


class Micrometer(Unit):
    def to(self, other_unit: str) -> float:
        if other_unit == 'nm':
            return self.quantity * 1000
        else:
            raise NotImplementedError('Could not convert units')


class Nanometer(Unit):
    def to(self, other_unit: str) -> float:
        if other_unit == 'um':
            return self.quantity / 1000
        else:
            raise NotImplementedError('Could not convert units')
