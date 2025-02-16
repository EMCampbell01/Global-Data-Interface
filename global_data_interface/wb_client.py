from typing import List
from global_data_interface.base_data_class import BaseDataClass
from global_data_interface.base_client import BaseClient
from dataclasses import asdict, dataclass
from global_data_interface.global_data_class import GlobalEconomy, GlobalIndicator


class WBAPIError(Exception):
    """Custom exception for WTO API errors."""
    pass


@dataclass
class WBIndicator(BaseDataClass):
    
    id: str
    name: str
    unit: str
    source: str
    sourceNote: str
    sourceOrganization: str
    topics: str
    
    def to_global(self):
        return GlobalIndicator(
            id = self.id,
            name = self.name,
            source = 'WB'
        )
 
    
@dataclass
class WBDataPoint(BaseDataClass):
    
    country: str
    country_id: str
    countryiso3code: str
    indicator: str
    date: str
    value: float
    unit: str
    obs_status: str
    decimal: int


@dataclass
class WBRegion(BaseDataClass):
    
    id: str
    code: str
    iso2code: str
    name: str


@dataclass
class WBIncomeLevel(BaseDataClass):
    
    id: str
    iso2code: str
    value: str


@dataclass
class WBEconomy(BaseDataClass):
    
    id: str
    iso2code: str
    name: str
    region: WBRegion
    adminRegion: any
    incomeLevel: WBIncomeLevel
    lendingType: any
    capitalCity: str
    longitude: float
    latitude: float
    
    def to_global(self):
        return GlobalEconomy(
            iso3 = self.id,
            iso2 = self.iso2code,
            name = self.name,
            sources = "WB"
        )
    

@dataclass
class WBTopic(BaseDataClass):
    
    id: int
    value: str
    sourceNote: str


@dataclass
class WBSource(BaseDataClass):
    
    id: int
    lastUpdated: str
    name: str
    code: str
    description: str
    dataAvailability: str
    metaDataAvailability: str
    concepts: int


class WBClient(BaseClient):
    '''A client for interacting with the WB API.'''
    
    BASE_URL = 'https://api.worldbank.org/v2'
    API_DOCS = 'https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information'
    
    def __init__(self):
        super().__init__('WB')
        
    def info(self) -> None:
        print(f'''
              WB API CLIENT INFO:
              
              BASE URL: {self.BASE_URL}
              API DOCS: {self.API_DOCS}
              ''')
    
    def indicators(self) -> List[WBIndicator]:
        '''Retrieves a list of available WB indicators.'''
        
        path_segments = ['/indicator']
        query_parameters = {'format': 'json', 'per_page': '1000'}
        url = self._construct_url(self.BASE_URL, path_segments, query_parameters)

        page = 1
        all_indicators = []

        while True:
            paged_url = self._add_query_parameters(url, {'page': page})

            try:
                response = self._get(paged_url)
                data = response.json()
            except WBAPIError as e:
                print(f"Error fetching WB indicators data: {e}")
                return []

            if data[1]:
                for item in data[1]:
                    all_indicators.append(WBIndicator(
                        id=item.get('id'),
                        name=item.get('name'),
                        unit=item.get('unit'),
                        source=item.get('source'),
                        sourceNote=item.get('sourceNote'),
                        sourceOrganization=item.get('sourceOrganization'),
                        topics=item.get('topics'),
                    ))
                    
            else:
                break

            page += 1

        return all_indicators
    
    def regions(self) -> List[WBRegion]:
        url = self.BASE_URL + '/region'
        url = self._add_query_parameters(url, {'format': 'json', 'per_page': '1000'})
        
        try:
            response = self._get(url)
            data = response.json()
        except WBAPIError as e:
            print(f"Error fetching WB regions data: {e}")
            return []
            
        if data[1]:
            regions = []
            for region in data[1]:
                regions.append(WBRegion(
                    id = region.get('id'),
                    code = region.get('code'),
                    iso2code = region.get('iso2code'),
                    name = region.get('name'),
                ))
            return regions
        else:
            print('WB Regions - Something went wrong.')
            return []
        
    def economies(self, region=None, income_level=None, lending_type=None) -> List[WBEconomy]:
        '''
        Retrieves a list of available WB economies.
        
        These are collected from the WB API "/country" endpoint, but contains economic zones which are not countries.
        '''
        
        path_segments = ['/country']
        query_parameters = {'format': 'json', 'per_page': '1000'}
        if region is not None:
            query_parameters['region'] = region
        if income_level is not None:
            query_parameters['income_level'] = income_level
        if lending_type is not None:
            query_parameters['lending_type'] = lending_type
        url = self._construct_url(self.BASE_URL, path_segments, query_parameters)
        
        try:
            response = self._get(url)
            data = response.json()
        except WBAPIError as e:
            print(f"Error fetching WB economies data: {e}")
            return []
        
        if data[1]:
            economies = []
            for economy in data[1]:
                economies.append(WBEconomy(
                    id = economy.get('id'),
                    iso2code = economy.get('iso2code'),
                    name = economy.get('name'),
                    region = economy.get('region'),
                    adminRegion = economy.get('adminRegion'),
                    incomeLevel = economy.get('incomeLevel'),
                    lendingType = economy.get('lendingType'),
                    capitalCity = economy.get('capitalCity'),
                    longitude = economy.get('longitude'),
                    latitude = economy.get('latitude'),
                ))
            return economies
        else:
            print('WB Economies - Something went wrong.')
            return []

    def topics(self) -> List[WBTopic]:
        '''
        Retrieves a list of available WB topics.
        
        WB indicators can be grouped by topic.
        '''
        
        path_segments = ['/topic']
        query_parameters = {'format': 'json', 'per_page': '1000'}
        url = self._construct_url(self.BASE_URL, path_segments, query_parameters)
        
        try:
            response = self._get(url)
            data = response.json()
        except WBAPIError as e:
            print(f"Error fetching WB topics data: {e}")
            return []
        
        if data[1]:
            topics = []
            for topic in data[1]:
                topics.append(WBTopic(
                    id = topic.get('id'),
                    value = topic.get('value'),
                    sourceNote = topic.get('sourceNote')
                ))
            return topics
        else:
            print('WB Topics - Something went wrong.')
            return []

    def sources(self) -> List[WBSource]:
        '''
        Retrieves a list of available WB sources.
        
        Note: WB indicators can be grouped by source.
        '''
        
        path_segments = ['/topic']
        query_parameters = {'format': 'json', 'per_page': '1000'}
        url = self._construct_url(self.BASE_URL, path_segments, query_parameters)
        
        try:
            response = self._get(url)
            data = response.json()
        except WBAPIError as e:
            print(f"Error fetching WB sources data: {e}")
            return []
        
        if data[1]:
            sources = []
            for source in data[1]:
                sources.append(WBSource(
                    id = source.get('id'),
                    lastUpdated = source.get('lastUpdated'),
                    name = source.get('name'),
                    code = source.get('code'),
                    description = source.get('description'),
                    dataAvailability = source.get('dataAvailability'),
                    metaDataAvailability = source.get('metaDataAvailability'),
                    concepts = source.get('concepts')
                ))
            return sources
        else:
            print('WB Sources - Something went wrong.')
            return []

    def income_levels(self) -> List[WBIncomeLevel]:
        url = self.BASE_URL + '/incomeLevel'
        url = self._add_query_parameters(url, {'format': 'json', 'per_page': '1000'})
        
        try:
            response = self._get(url)
            data = response.json()
        except WBAPIError as e:
            print(f"Error fetching WB income levels data: {e}")
            return []
        
        if data[1]:
            income_levels = []
            for income_level in data[1]:
                income_levels.append(WBIncomeLevel(
                    id = income_level.get('id'),
                    iso2code = income_level.get('iso2code'),
                    value = income_level.get('value'),         
                ))
            return income_levels
        else:
            print('WB Income Levels - Something went wrong.')
            return []

    
    def data(self, countries, indicators, start_date, end_date, frequency='Y'):
        '''
        Retrieves time series data for the specified countries and indicators within the given date range.
        
        Args:
            countries (list): A list of country codes.
            indicators (list): A list of indicator codes.
            start_date (int): The start year for the time series data.
            end_date (int): The end year for the time series data.
            frequency (str): Frequency of data (default is 'Y' for yearly data).
        
        Returns:
            list: A list of dictionaries containing the time series data for each country and indicator.
        '''
        # Convert the list of countries and indicators to a comma-separated string
        country_codes = ';'.join(countries)
        indicator_codes = ';'.join(indicators)

        # Construct the URL for the time series data
        # url = f'{self.BASE_URL}/country/{country_codes}/indicator/{indicator_codes}'
        # url = self._add_query_parameters(url, {
        #     'date': f'{start_date}:{end_date}',
        #     'format': 'json',
        #     'frequency': frequency,
        #     'per_page': '1000'
        # })
        
        query_parameters = {
            'date': f'{start_date}:{end_date}',
            'format': 'json',
            'frequency': frequency,
            'per_page': '1000'
        }
        
        url = self._construct_url(self.BASE_URL, ['country', country_codes, 'indicator', indicator_codes],  query_parameters)
        
        page = 1
        all_data_points = []

        while True:
            # Add pagination query parameter
            paged_url = self._add_query_parameters(url, {'page': page})
            response = self._get(paged_url)
            data = response.json()

            # Check if the data contains values (data[1] is where the time series data is)
            if data and len(data) > 1 and data[1]:
                for entry in data[1]:
                    all_data_points.append(WBDataPoint(
                        country=entry['country']['value'],
                        country_id=entry['country']['id'],
                        countryiso3code=entry.get('countryiso3code'),
                        indicator=entry['indicator']['value'],
                        date=entry.get('date'),
                        value=entry.get('value'),
                        unit=entry.get('unit'),
                        obs_status=entry.get('obs_status'),
                        decimal=entry.get('decimal')
                    ))
            else:
                break

            page += 1

        return all_data_points

