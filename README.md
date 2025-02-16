# GLOBAL DATA INTERFACE

[![Version](https://img.shields.io/badge/version-0.1.0a1-orange)](https://github.com/EMCampbell01/Global-Data-Interface)
[![Downloads](https://img.shields.io/pypi/dm/Global-Data-Interface)](https://pypi.org/project/Global-Data-Interface/)

Global Data Interface is a Python package designed to provide a unified interface to easily query for data from a number of APIs providing international time series data.

## README Contents

- [Installation](#Installation)
- [Usage](#Usage)
    - [Global Data](#global-data)
    - [World Bank Data](#world-bank-data)
- [Design](#design)
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

## Global Data

## API Specific Data 

### World Bank Data

The `WBClient` is an attribute of `GlobalDataClient` and can be used individually to retrive WB specific data.

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

The UN Client is still to be implemented.

## Data-Structures

