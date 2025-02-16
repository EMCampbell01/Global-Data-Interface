from global_data_interface.global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()

imf_indicators = gdi.imf.indicators()
print(f'IMF Indicator Count: {len(imf_indicators)}\n{imf_indicators}')

# Government expenditure, percent of GDP
# data = gdi.imf.data('exp', countries=['GBR'], years=['2000', '2010', '2020'])

# print(data[0])