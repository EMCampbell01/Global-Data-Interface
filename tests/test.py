from global_data_interface.global_data_interface import GlobalDataInterface
import sys

if __name__ == "__main__":


    gdi = GlobalDataInterface()
    
    test_wb_client = True
    test_imf_client = False
    test_wto_client = False
    test_global_interface = False
    

    if test_wb_client:
        
        gdi.wb.info()
        
        wb_indicators = gdi.wb.indicators()
        wb_economies = gdi.wb.economies()
        wb_regions = gdi.wb.regions()
        wb_topics = gdi.wb.topics()
        wb_income_levels = gdi.wb.income_levels()
        wb_sources = gdi.wb.sources()
        
        print(f"WB regions: {len(wb_regions)}")
        print(f"WB economies: {len(wb_economies)}")
        print(f"WB topics: {len(wb_topics)}")
        print(f"WB income levels: {len(wb_income_levels)}")
        print(f"WB sources: {len(wb_sources)}")
        print(f"WB indicators: {len(wb_indicators)}")
        
        countries = ['USA', 'BRA']
        indicators = ['NY.GDP.MKTP.CD', 'FP.CPI.TOTL.ZG']

        start_date = 2018
        end_date = 2020
        
        data = gdi.wb.data(countries, indicators, start_date, end_date)
        for i in data:
            print(i)
        
    if test_imf_client:
        
        imf_indicators = gdi.imf.indicators()
        imf_countries = gdi.imf.economies()
        
        imf_groups = gdi.imf.groups()
        imf_regions = gdi.imf.regions()
        
        print(f"Number of IMF countries: {len(imf_countries)}")
        print(f"Number of IMF groups: {len(imf_groups)}")
        print(f"Number of IMF regions: {len(imf_regions)}")
        print(f"Number of IMF indicators: {len(imf_indicators)}")

        print(imf_countries[0], imf_countries[1], imf_countries[2])
        print(imf_indicators[0], imf_indicators[1], imf_indicators[2])

        countries = ['USA', 'BRA']
        indicator = 'NGDPD'
        years = ['2015', '2016', '2017']
        
        data = gdi.imf.data(indicator, countries=countries, years=years)
        print(f'Data: {data}')
        for i in data:
            print(i)
        
    if test_wto_client:
        
        wto_indicators = gdi.wto.indicators()
        wto_economies = gdi.wto.economies()
        
        wto_economic_groups = gdi.wto.economic_groups()
        wto_geographical_regions = gdi.wto.geographical_regions()
        wto_topics = gdi.wto.topics()
        wto_indicator_catagories = gdi.wto.indicator_catagories()
        wto_products_and_sectors = gdi.wto.products_and_sectors()
        wto_units = gdi.wto.units()
        
        data = gdi.wto.data()
        
    if test_global_interface:
        
        indicators = gdi.indicators()
        economies = gdi.economies()
        for i in economies:
            print(i)
        print(len(economies))
        
    sys.exit()
