# GLOBAL DATA INTERFACE

[![Version](https://img.shields.io/badge/version-0.1.0a1-orange)](https://github.com/EMCampbell01/Global-Data-Interface)
[![Downloads](https://img.shields.io/pypi/dm/Global-Data-Interface)](https://pypi.org/project/Global-Data-Interface/)

Global Data Interface is a Python package designed to provide a unified interface to easily query for data from a number of APIs providing international time series data.

## README Contents

- [Installation](#Installation)
- [Usage](#Usage)
    - [World Bank Data](#world-bank-data)
    - [International Monetary Fund Data](#international-monetary-fund-data)
    - [World Trade Organization Data](#world-trade-organization-data)
    - [United Nations Data](#united-nations-data)
    - [Global Data](#global-data)
- [Package Design](#design)
    - [Global Data Interface](#global-data-interface-1)
    - [Sub-Clients](#sub-clients)
    - [Data-Structures](#data-structures)

## Installation

Avaliable on Pypi:

https://pypi.org/project/Global-Data-Interface/

Download via pip:
```bash
pip install Global-Data-Interface
```

---

# Usage

## API Specific Data 

### World Bank Data

The `WBClient` can be used individually to retrive WB specific data. 

**Examples:**

Retrive WB Indicators:
```python
from global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()
wb_indicators = gdi.wb.indicators()
print(f'WB Indicator Count: {len(wb_indicators)}\n{wb_indicators[0]}')
```
```
WB Indicator Count: 24604
{'id': '1.0.HCount.1.90usd', 'name': 'Poverty Headcount ($1.90 a day)', 'unit': '', 'source': {'id': '37', 'value': 'LAC Equity Lab'}, 'sourceNote': 'The poverty headcount index measures the proportion of the population with daily per capita income (in 2011 PPP) below the poverty line.', 'sourceOrganization': 'LAC Equity Lab tabulations of SEDLAC (CEDLAS and the World Bank).', 'topics': [{'id': '11', 'value': 'Poverty '}]}
```


Retrive WB economies in the EU area:
```python
from global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()
wb_euro_area_economies = gdi.wb.economies(region='EMU')
print(f'{wb_euro_area_economies[0]}')
```
```
{'id': 'AUT', 'iso2code': None, 'name': 'Austria', 'region': {'id': 'ECS', 'iso2code': 'Z7', 'value': 'Europe & Central Asia'}, 'adminRegion': None, 'incomeLevel': {'id': 'HIC', 'iso2code': 'XD', 'value': 'High income'}, 'lendingType': {'id': 'LNX', 'iso2code': 'XX', 'value': 'Not classified'}, 'capitalCity': 'Vienna', 'longitude': '16.3798', 'latitude': '48.2201'}
```


Retrive WB GDP for 2020 from the United States and China:
```python
from global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()

countries = ['USA', 'CHN']
indicators = ['NY.GDP.MKTP.CD']
start_date = 2022
end_date = 2022

data = gdi.wb.data(countries, indicators, start_date, end_date)
for data_point in data:
    print(data_point)
```
```
{'country': 'China', 'country_id': 'CN', 'countryiso3code': 'CHN', 'indicator': 'GDP (current US$)', 'date': '2022', 'value': 17881782683707.3, 'unit': '', 'obs_status': '', 'decimal': 0}
{'country': 'United States', 'country_id': 'US', 'countryiso3code': 'USA', 'indicator': 'GDP (current US$)', 'date': '2022', 'value': 26006893000000, 'unit': '', 'obs_status': '', 'decimal': 0}
```

### International Monetary Fund Data

The `IMFClient` can be used individually to retrive IMF specific data. 

**Examples:**

Retrive IMF Indicators:
```python
from global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()

imf_indicators = gdi.imf.indicators()
print(f'IMF Indicator Count: {len(imf_indicators)}\n{imf_indicators[0]}')
```
```
{'code': 'NGDP_RPCH', 'label': 'Real GDP growth', 'description': "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at constant prices of final goods and services produced within a country during a specified time period, such as one year.", 'source': 'World Economic Outlook (October 2024)', 'unit': 'Annual percent change', 'dataset': 'WEO'}
```

Retrive government expenditure as a percent of GDP for the UK in 2010 and 2020:
```python
from global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()

data = gdi.imf.data('exp', countries=['GBR'], years=['2010', '2020'])
print(f'{data[0]}\n{data[1]}')
```
```
{'area_code': 'GBR', 'indicator_code': 'exp', 'year': 2010, 'value': 50.562698364258}
{'area_code': 'GBR', 'indicator_code': 'exp', 'year': 2020, 'value': 49.866941221865}
```

### World Trade Organization Data

The `WTOClient` can be used individually to retrive WTO specific data. 

Retrive WTO economic groups:
```python
from global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()

wto_economic_groups = gdi.wto.economic_groups()
print(wto_economic_groups[9])
```
```
{'code': '918', 'name': 'European Union', 'displayOrder': 1240}
```

Retrive WTO economies in the EU economic group:
```python
from global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()

wto_eu_economies = gdi.wto.economies(gp='918')
print(wto_eu_economies[0])
```
```
{'code': '040', 'iso3A': 'AUT', 'name': 'Austria', 'displayOrder': 220}
```

### United Nations Data

The UN Client is still to be fully implemented.

## Global Data


---

# Design

## Global Data Interface

The `GlobalDataInterface` class is the main interface for the package. It is a singleton class. The `GlobalDataInterface` contains several sub-clients which each interact with and retrive data from their associated API. A `GlobalDataInterface` object can be used to interact with each of its internal sub-clients individually to create API specific requests and retrive API specific data.

The `GlobalDataInterface` has the following methods to retrive data from multiple sub-clients, and return data in a unified structure.

- `indicators()`
- `economies()`
- `indicator_groups()`
- `economy_groups()`
- `data()`

## Sub-Clients

In its current version `GlobalDataInterface` has 4 sub-clients for the following organizations and their APIs:

- `WBClient`
- `UNClient`
- `WTOClient`
- `IMFClient`

these all inheriate from the `BaseClient` abstract class. The `BaseClient` contains internal utility methods for url construction and making REST HTTP requests. The `BaseClient` contains an abstract method `info()` which is implemented in child classes to print details om the specific API being interacted with, including the organization providing it and a link to its documentation.

**World Bank Client**

The WB client provides methods for retreiving data from the WB V2 API endpoints.

- `indicators()`
- `economies()`
- `regions()`
- `topics()`
- `sources()`
- `income_levels()`
- `data()`

**World Trade Organization Client**

The WTO Client provides methods for retreving data from the WTO timeseries V1 API endpoints.

- `indicators()`
- `economies()`
- `indicator_catagories()`
- `regions()`
- `economic_groups()`
- `product_classifications()`
- `products_and_sectors()`
- `topics()`
- `units()`
- `periods()`
- `frequencies()`
- `data()`

**International Monetary Fund Client**

The IMF Client provides methods for retreving data from the IMF datamapper V1 API endpoints.

- `indicators()`
- `economies()`
- `regions()`
- `groups()`
- `data()`

**United Nations Client**

The UN Client is still to be fully implemented.

## Data-Structures

