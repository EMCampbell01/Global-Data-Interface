from global_data_interface.global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()

# wb_indicators = gdi.wb.indicators()

# print(f'WB Indicator Count: {len(wb_indicators)}')
# print(wb_indicators[0])

# wb_regions = gdi.wb.regions()
# print(f'WB Regions:\n{wb_regions}')

# wb_east_asian_economies = gdi.wb.economies(region='EMU')
# print(f'WB East Asian Economies:\n{wb_east_asian_economies[0]}')

countries = ['USA', 'CHN']
indicators = ['NY.GDP.MKTP.CD']
start_date = 2022
end_date = 2022

data = gdi.wb.data(countries, indicators, start_date, end_date)
for data_point in data:
    print(data_point)