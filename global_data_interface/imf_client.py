from global_data_interface.base_data_class import BaseDataClass
from global_data_interface.base_client import BaseClient
from global_data_interface import GlobalEconomy, GlobalIndicator
from dataclasses import asdict, dataclass
from typing import List


class IMFAPIError(Exception):
    '''Custom exception for WTO API errors.'''
    pass

@dataclass
class IMFTimeseriesDatapoint:
    
    area_code: str
    indicator_code: str
    year: int
    value: float

    def __str__(self):
        return (str(self.to_dict()))
    
    def to_dict(self):
        return asdict(self)

@dataclass
class IMFIndicator:
    
    code: str
    label: str
    description: str
    source: str
    unit: str
    dataset: str
    
    def __str__(self):
        return (str(self.to_dict()))
    
    def to_dict(self):
        return asdict(self)
    
    def to_global(self):
        return GlobalIndicator(
            id = self.code,
            name = self.label,
            source = 'IMF'
        )

@dataclass
class IMFCountry(BaseDataClass):
    
    code: str
    label: str
    
    def to_global(self):
        return GlobalEconomy(
            iso3 = self.code,
            name = self.label,
            sources = "IMF"
        )

@dataclass
class IMFRegion:
    
    code: str
    label: str
    
    def __str__(self):
            return (f'{self.code}, {self.label}')
    
    def to_dict(self):
        return asdict(self)

@dataclass
class IMFGroup:
    
    code: str
    label: str
    
    def __str__(self):
            return (f'{self.code}, {self.label}')
    
    def to_dict(self):
        return asdict(self)

class IMFClient(BaseClient):
    '''A client for interacting with the IMF API.'''
    
    BASE_URL = 'https://www.imf.org/external/datamapper/api/v1'
    API_DOCS = 'https://www.imf.org/external/datamapper/api/help'

    def __init__(self):
        super().__init__('IMF')
        
    def info(self) -> None:
        print(f'''
              WB API CLIENT INFO:
              
              BASE URL: {self.BASE_URL}
              API DOCS: {self.API_DOCS}
              ''')
    
    def data(self, indicator: str, countries: List[str] = None, regions: List[str] = None, groups: List[str] = None, years: List[int] = None) -> List[IMFTimeseriesDatapoint]:
        '''
        Fetches timeseries data for a given indicator, filtered by countries, regions, groups, and years.

        Args:
            indicator (str): The indicator code (e.g., 'PPPGDP').
            countries (List[str]): List of country codes to filter by.
            regions (List[str]): List of region codes to filter by.
            groups (List[str]): List of group codes to filter by.
            years (List[int]): List of years to filter by.

        Returns:
            List[IMFTimeseriesDatapoint]: A list of IMFTimeseriesDatapoint objects.
        '''
        path_segments = [indicator]
        if countries:
            path_segments += countries
        if regions:
            path_segments += regions
        if groups:
            path_segments += groups
        print(f"Path segments: {path_segments}")
        url = self._add_path_segments(self.BASE_URL, path_segments)
        
        print("URL: ", url)

        try:
            response = self._get(url)
            data = response.json()
        except IMFAPIError as e:
            print(f'Error fetching IMF timeseries data: {e}')
            return []

        timeseries_data = []
        indicator_data = data.get('values', {}).get(indicator, {})
        
        for area_code, year_values in indicator_data.items():
            for year, value in year_values.items():
                datapoint = IMFTimeseriesDatapoint(
                    area_code=area_code,
                    indicator_code=indicator,
                    year=int(year),
                    value=float(value)
                )
                timeseries_data.append(datapoint)

        return timeseries_data
        
    
    def indicators(self):
        '''Retrieves a list of available indicators.

        Returns:
            list: A list of IMFIndicator instances.
        '''
        url = self.BASE_URL + '/indicators'

        try:
            response = self._get(url)
            data = response.json()
        except IMFAPIError as e:
            print(f'Error fetching IMF indicators: {e}')
            return []

        return [
            IMFIndicator(
                code=indicator_code,
                label=indicator_data.get('label'),
                description=indicator_data.get('description', ''),
                source=indicator_data.get('source', ''),
                unit=indicator_data.get('unit', ''),
                dataset=indicator_data.get('dataset', '')
            )
            for indicator_code, indicator_data in data.get('indicators').items()
        ]
    
    def economies(self):
        '''Retrieves a list of available countries.

        Returns:
            list: A list of IMFCountry instances.
        '''
        url = self.BASE_URL + '/countries'

        try:
            response = self._get(url)
            data = response.json()
        except IMFAPIError as e:
            print(f'Error fetching IMF Countries: {e}')
            return []

        return [
            IMFCountry(
                code=country_code,
                label=country_data.get('label')
            )
            for country_code, country_data in data.get('countries').items()
        ]
    
    def regions(self):
        
        url = self.BASE_URL + '/regions'
        
        try:
            response = self._get(url)
            data = response.json()
        except IMFAPIError as e:
            print(f'Error fetching IMF Regions: {e}')
            return []
        
        return [
            IMFRegion(
                code=region_code,
                label=region_data.get('label')
            )
            for region_code, region_data in data.get('regions').items()
        ]
    
    def groups(self):
        '''Retrieves a list of available analytical groups.

        Returns:
            list: A list of IMFGroup instances.
        '''
        url = self.BASE_URL + '/groups'

        try:
            response = self._get(url)
            data = response.json()
        except IMFAPIError as e:
            print(f'Error fetching IMF Groups: {e}')
            return []

        return [
            IMFGroup(
                code=group_code,
                label=group_data.get('label')
            )
            for group_code, group_data in data.get('groups').items()
        ]