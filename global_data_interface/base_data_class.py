from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass


@dataclass
class BaseDataClass(ABC):
    
    def __str__(self):
        return (str(self.to_dict()))
            
    def to_dict(self):
        return asdict(self)
    
    def to_global(self):
        pass