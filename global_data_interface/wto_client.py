from dataclasses import asdict, dataclass
from urllib.parse import urlencode
import requests

from global_data_interface.base_client import BaseClient
from global_data_interface.base_data_class import BaseDataClass
from global_data_interface.global_data_class import GlobalEconomy, GlobalIndicator

class WTOAPIError(Exception):
    """Custom exception for WTO API errors."""
    pass

@dataclass
class WTOProductClassification:
    
    code: str
    name: str
    
    def __str__(self):
            return (f"{self.name} ({self.code})")
    
    def to_dict(self):
        return asdict(self)

@dataclass
class WTOProduct:
    
    code: str
    name: str
    note: str
    productClassification: str
    codeUnique: str
    displayOrder: int
    hierarchy: int

    def __str__(self):
            return (f"{self.name} ({self.code})")
    
    def to_dict(self):
        return asdict(self)


@dataclass
class WTOTimeseriesDatapoint:
    
    indicatorCategoryCode: str
    indicatorCategory: str
    indicatorCode: str
    indicator: str
    reportingEconomyCode: str
    reportingEconomy: str
    partnerEconomyCode: str
    partnerEconomy: str
    productOrSectorClassificationCode: str
    productOrSectorClassification: str
    productOrSectorCode: str
    productOrSector: str
    periodCode: str
    period: str
    frequencyCode: str
    frequency: str
    unitCode: str
    unit: str
    year: int
    valueFlagCode: str
    valueFlag: str
    textValue: str
    value: int
    
    def __str__(self):
        return (f"{self.year} {self.indicator} {self.productOrSector} {self.productOrSectorCode} {self.period} {self.unit} {self.reportingEconomy} ({self.partnerEconomy}) {self.value}")

    def to_dict(self):
        return asdict(self)

@dataclass
class WTOUnit:
    
    code: str
    name: str

    def __str__(self):
            return (f"{self.name} ({self.code})")
    
    def to_dict(self):
        return asdict(self)

@dataclass
class WTOIndicatorCategory:
    
    code: str
    name: str
    parentCode: str
    sortOrder: int
    
    def __str__(self):
            return (f"{self.name} ({self.code})")
    
    def to_dict(self):
        return asdict(self)

@dataclass
class WTOIndicator:
    
    code: str
    name: str
    categoryCode: str
    categoryLabel: str
    subcategoryCode: str
    subcategoryLabel: str
    unitCode: str
    unitLabel: str
    startYear: int
    endYear: int
    frequencyCode: str
    frequencyLabel: str
    numberReporters: int
    numberPartners: int
    productSectorClassificationCode: str
    productSectorClassificationLabel: str
    hasMetadata: str
    numberDecimals: int
    numberDatapoints: int
    updateFrequency: str
    description: str
    sortOrder: int
    
    def __str__(self):
        return (str(self.to_dict()))
            
    def to_dict(self):
        return asdict(self)
    
    def to_global(self):
        return GlobalIndicator(
            id = self.code,
            name = self.name,
            source = 'WTO'
        )

@dataclass
class WTOGeographicalRegion:
    
    code: str
    name: str
    displayOrder: int
    
    def __str__(self):
            return (f"{self.name} ({self.code})")
        
    def to_dict(self):
        return asdict(self)
    
@dataclass
class WTOTerritory(BaseDataClass):
    
    code: str
    iso3A: str
    name: str
    displayOrder: int
    
    def to_global(self):
        return GlobalEconomy(
            iso3 = self.iso3A,
            name = self.name,
            sources = "WTO"
        )

class WTOClient(BaseClient):
    """A client for interacting with the WTO API."""
    
    BASE_URL = "http://api.wto.org/timeseries/v1"
    API_DOCS = 'https://apiportal.wto.org/api-details#api=version1'
    
    def __init__(self):
        headers = {"Ocp-Apim-Subscription-Key": '57e24c1ab6c44521b3c3c28d80f83462'}
        super().__init__('IMF', headers=headers)
        
    def info(self) -> None:
        print(f'''
              WTP API CLIENT INFO:
              
              BASE URL: {self.BASE_URL}
              API DOCS: {self.API_DOCS}
              ''')

    def data(self, i, r=None, p=None, ps=None, pc=None, spc=None, fmt=None, mode=None, dec=None, off=None, max=None, head=None, lang=None, meta=None) -> list[WTOTimeseriesDatapoint]:
        """
        Args:
            i (): Indicator code.
            r (): Reporting economies (comma separated codes).
            p (): Partner economies where applicable (comma separated codes).
            ps (): Time period.
            pc (): Products/sectors (comma separated codes) where applicable.
            spc (): Include sub products/sectors. If true, all child items in the product/sector hierarchy are recursively included.
            fmt (): Output format.
            mode (): Output mode.
            dec (): Number of decimals.
            off (): Number of records to skip (offset). You can use it for implementing pagination.
            max (): Maximum number of records to return.
            head (): Heading style.
            lang (): Language id.
            meta (): Include Metadata information. If enabled, it will generate additional files/arrays.
        Returns:
            list[WTOTimeseriesDatapoint]:
        """

        url = self.BASE_URL + "/data"
        payload = {key: value for key, value in {
            "i": i,
            "r": r,
            "p": p,
            "ps": ps,
            "pc": pc,
            "spc": spc,
            "fmt": fmt,
            "mode": mode,
            "dec": dec,
            "off": off,
            "max": max,
            "head": head,
            "lang": lang,
            "meta": meta
        }.items() if value is not None}
        
        try:
            response = self._post(url, payload)
            data = response.json()
        except WTOAPIError as e:
            print(f"Error fetching timeseries datapoints for indicator {i}: {e}")
            return []
        
        return [
            WTOTimeseriesDatapoint(
                indicatorCategoryCode=datapoint.get("IndicatorCategoryCode"),
                indicatorCategory=datapoint.get("IndicatorCategory"),
                indicatorCode=datapoint.get("IndicatorCode"),
                indicator=datapoint.get("Indicator"),
                reportingEconomyCode=datapoint.get("ReportingEconomyCode"),
                reportingEconomy=datapoint.get("ReportingEconomy"),
                partnerEconomyCode=datapoint.get("PartnerEconomyCode"),
                partnerEconomy=datapoint.get("PartnerEconomy"),
                productOrSectorClassificationCode=datapoint.get("ProductOrSectorClassificationCode"),
                productOrSectorClassification=datapoint.get("ProductOrSectorClassification"),
                productOrSectorCode=datapoint.get("ProductOrSectorCode"),
                productOrSector=datapoint.get("ProductOrSector"),
                periodCode=datapoint.get("PeriodCode"),
                period=datapoint.get("Period"),
                frequencyCode=datapoint.get("FrequencyCode"),
                frequency=datapoint.get("Frequency"),
                unitCode=datapoint.get("UnitCode"),
                unit=datapoint.get("Unit"),
                year=datapoint.get("Year"),
                valueFlagCode=datapoint.get("ValueFlagCode"),
                valueFlag=datapoint.get("ValueFlag"),
                textValue=datapoint.get("TextValue"),
                value=datapoint.get("Value"),
            )
            for datapoint in data.get('Dataset', [])
        ]

    def get_timeseries_data_count(self):
        pass

    def get_timeseries_metadata(self):
        pass

    def topics(self):
        pass

    def frequencies(self):
        pass

    def periods(self):
        pass

    def units(self, lang: str = None):
        
        url = self.BASE_URL + "/units"
        url = self._add_query_parameters(url, {"lang": lang})
        
        try:
            response = self._get(url)
            data = response.json()
        except WTOAPIError as e:
            print(f"Error fetching units: {e}")
            return []
        
        return [
            WTOUnit(
                code=unit.get("code"),
                name=unit.get("name"),
            )
            for unit in data
        ]

    def indicator_catagories(self, lang: str = None) -> list[WTOIndicatorCategory]:
        
        url = self.BASE_URL + "/indicator_categories"
        url = self._add_query_parameters(url, {"lang": lang})
        
        try:
            response = self._get(url)
            data = response.json()
        except WTOAPIError as e:
            print(f"Error fetching indicator catagories: {e}")
            return []
        
        return [
            WTOIndicatorCategory(
                code=category.get("code"),
                name=category.get("name"),
                parentCode=category.get("parentCode"),
                sortOrder=category.get("sortOrder")
            )
            for category in data
        ]
        
    def indicators(self, i=None, name=None, t=None, pc=None, tp=None, frq=None, lang=None) -> list[WTOIndicator]:
        """
        Args:
            i (str, optional): Indicator Code. Filter on one specific indicator.
            name (str, optional): Indicator name (or part of the name).
            t (str, optional): Topics (comma separated ids).
            pc (): Product Classifications.
            tp (): Trade partner.
            frq (): Frequency.
            lang (): Language id.
            
        Returns:
            list[Indicator]: A list of Indicator objects representing the retrieved indicators.
        """
        
        url = self.BASE_URL + "/indicators"
        params = {
            "i": i,
            "name": name,
            "t": t,
            "pc": pc,
            "tp": tp,
            "frq": frq,
            "lang": lang
        }
        url = self._add_query_parameters(url, params)
        
        try:
            response = self._get(url)
            data = response.json() 
        except WTOAPIError as e:
            print(f"Error fetching indicators: {e}")
            return []
        
        return [
            WTOIndicator(
                code=indicator.get("code"),
                name=indicator.get("name"),
                categoryCode=indicator.get("categoryCode"),
                categoryLabel=indicator.get("categoryLabel"),
                subcategoryCode=indicator.get("subcategoryCode"),
                subcategoryLabel=indicator.get("subcategoryLabel"),
                unitCode=indicator.get("unitCode"),
                unitLabel=indicator.get("unitLabel"),
                startYear=indicator.get("startYear"),
                endYear=indicator.get("endYear"),
                frequencyCode=indicator.get("frequencyCode"),
                frequencyLabel=indicator.get("frequencyLabel"),
                numberReporters=indicator.get("numberReporters"),
                numberPartners=indicator.get("numberPartners"),
                productSectorClassificationCode=indicator.get("productSectorClassificationCode"),
                productSectorClassificationLabel=indicator.get("productSectorClassificationLabel"),
                hasMetadata=indicator.get("hasMetadata"),
                numberDecimals=indicator.get("numberDecimals"),
                numberDatapoints=indicator.get("numberDatapoints"),
                updateFrequency=indicator.get("updateFrequency"),
                description=indicator.get("description"),
                sortOrder=indicator.get("sortOrder")
            )
            for indicator in data
        ]
        
    def geographical_regions(self, lang: str = None) -> list[WTOGeographicalRegion]:
        """Fetches a list of geographical regions from the WTO API.

        Args:
            lang (str, optional): The language code for the response. 
                Language id:
                    1 : English
                    2 : French
                    3 : Spanish
                Defaults to None.

        Returns:
            list[GeographicalRegion]: A list of GeographicalRegion objects representing the retrieved regions.
        """
        
        url = self.BASE_URL + "/territory/regions"
        url = self._add_query_parameters(url, {"lang": lang})

        try:
            response = self._get(url)
            data = response.json()
        except WTOAPIError as e:
            print(f"Error fetching geographical regions: {e}")
            return []
        
        return [
            WTOGeographicalRegion(
                code=region.get("code"),
                name=region.get("name"),
                displayOrder=region.get("displayOrder")
            )
            for region in data
        ]
    
    def economic_groups(self):
        pass
    
    def economies(self, name=None, ig=None, reg=None, gp=None, lang=None):
        
        url = self.BASE_URL + "/reporters"
        params = {
            "name": name,
            "ig": ig,
            "reg": reg,
            "gp": gp,
            "lang": lang
        }
        url = self._add_query_parameters(url, params)
        
        try:
            response = self._get(url)
            data = response.json() 
        except WTOAPIError as e:
            print(f"Error fetching reporting economies: {e}")
            return []
        
        return [
            WTOTerritory(
                code=territory.get("code"),
                iso3A=territory.get("iso3A"),
                name=territory.get("name"),
                displayOrder=territory.get("displayOrder")
            )
            for territory in data
        ]
    
    def product_classifications(self, lang: str = None):
        
        url = self.BASE_URL + '/product_classifications'
        url = self._add_query_parameters(url, {"lang": lang})
        
        try:
            response = self._get(url)
            data = response.json()
        except WTOAPIError as e:
            print(f"Error fetching indicator catagories: {e}")
            return []
        
        return [
            WTOProductClassification(
                code=productClassification.get("code"),
                name=productClassification.get("name")
            )
            for productClassification in data
        ]
        
    
    def products_and_sectors(self, name=None, pc=None, lang=None):
        
        url = self.BASE_URL + "/products"
        params = {
            "name": name,
            "pc": pc,
            "lang": lang
        }
        url = self._add_query_parameters(url, params)

        try:
            response = self._get(url)
            data = response.json() 
        except WTOAPIError as e:
            print(f"Error fetching reporting economies: {e}")
            return []
        
        return [
            WTOProduct(
                code = territory.get("code"),
                name = territory.get("name"),
                note = territory.get("note"),
                productClassification = territory.get("productClassification"),
                codeUnique = territory.get("codeUnique"),
                displayOrder = territory.get("displayOrder"),
                hierarchy = territory.get("hierarchy"),
            )
            for territory in data
        ]

    