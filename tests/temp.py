from global_data_interface.global_data_interface import GlobalDataInterface

gdi = GlobalDataInterface()

wb_indicators = gdi.wb.indicators()

print(f'WB Indicator Count: {len(wb_indicators)}')
print(wb_indicators[0])