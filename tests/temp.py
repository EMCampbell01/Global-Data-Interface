from global_data_interface.global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()

# imf_indicators = gdi.imf.indicators()
# print(f'IMF Indicator Count: {len(imf_indicators)}\n{imf_indicators[0]}')

# Government expenditure, percent of GDP
# data = gdi.imf.data('exp', countries=['GBR'], years=['2010', '2020'])

# print(f'{data[0]}\n{data[1]}')

# wto_economic_groups = gdi.wto.economic_groups()
# print(wto_economic_groups)


# 962
# 900
# 937

# wto_eu_economies = gdi.wto.economies(gp='918')
# print(wto_eu_economies[0])

indicators = gdi.wto.indicators()
print(indicators[0])

wto_data = gdi.wto.data('TP_A_0010')
for i in wto_data:
    print(i)