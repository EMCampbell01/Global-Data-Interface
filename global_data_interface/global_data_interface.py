from global_data_interface import *
from typing import List
import uuid


class GlobalDataInterface:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalDataInterface, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.wb = WBClient()
        self.wto = WTOClient()
        self.imf = IMFClient()
        self.un = UNClient()
        
    def indicators(self, sources=['WB', 'WTO', 'IMF', 'UN']) -> List[GlobalIndicator]:
        '''
        '''
                
        source_mapping = {
            'WB': self.wb,
            'WTO': self.wto,
            'IMF': self.imf,
            'UN': self.un
        }
        
        all_indicators = []
        
        for source in sources:
            if source in source_mapping:
                all_indicators += source_mapping[source].indicators()
        
        return [indicator.to_global() for indicator in all_indicators]
    
    def economies(self, sources=['WB', 'WTO', 'IMF']) -> List[GlobalEconomy]:
        
        economies = []
        
        if 'WB' in sources:
            economies += self.wb.economies()
            
        if 'WTO' in sources:
            economies += self.wto.economies()
            
        if 'IMF' in sources:
            economies += self.imf.economies()
            
        all_global_economies = [economy.to_global() for economy in economies]
        
        merged_global_economies = {}
        for economy in all_global_economies:
            if not economy.iso3:
                merged_global_economies[uuid.uuid4()] = economy
            elif economy.iso3 not in merged_global_economies.keys():
                merged_global_economies[economy.iso3] = GlobalEconomy(iso3=economy.iso3, name=set([economy.name]), sources=set([economy.sources]))
            else:
                merged_global_economies[economy.iso3].name.add(economy.name)
                merged_global_economies[economy.iso3].sources.add(economy.sources)
        
        return merged_global_economies.values()
    
    def indicator_groups(self, sources=['WB', 'WTO', 'IMF']):
        pass
    
    def economy_groups(self, sources=['WB', 'WTO', 'IMF']):
        pass
    
    def data(self, indicators:List[GlobalIndicator], years:List[int], economies, indicator_groups, economy_groups):
        
        catagorized_indicators = {'WB': [], 'WTO': [], 'IMF': []}
        for indicator in indicators:
            if indicator.source in catagorized_indicators.keys():
                catagorized_indicators[indicator.source].append(indicator)