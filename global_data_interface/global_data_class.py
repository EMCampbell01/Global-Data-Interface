from abc import ABC
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class GlobalDataClass(ABC):
    
    def __str__(self):
        return (str(self.to_dict()))
            
    def to_dict(self):
        return asdict(self)

@dataclass
class GlobalIndicator(GlobalDataClass):
    
    id: str
    name: str
    source: str

@dataclass
class GlobalEconomy(GlobalDataClass):
    
    iso3: Optional[str] = None
    iso2: Optional[str] = None
    name: Optional[str] = None
    sources: Optional[str] = None

@dataclass
class GlobalDataPoint(GlobalDataClass):
    
    indicator: str
    time: str
    value: float

@dataclass
class GlobalEconomyGroup(GlobalDataClass):
    
    id: str

@dataclass
class GlobalIndicatorGroup(GlobalDataClass):
    pass

