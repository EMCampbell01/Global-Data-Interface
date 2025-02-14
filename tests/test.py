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
        
        # wb_economies = client.wb.economies()
        
        # wb_regions = client.wb.regions()
        # wb_topics = client.wb.topics()
        # wb_income_levels = client.wb.income_levels()
        # wb_sources = client.wb.sources()
        
        # # data = client.wb.data()
        
        # print(f"Number of WB regions: {len(wb_regions)}")
        # print(f"Number of WB economies: {len(wb_economies)}")
        # print(f"Number of WB topics: {len(wb_topics)}")
        # print(f"Number of WB income levels: {len(wb_income_levels)}")
        # print(f"Number of WB sources: {len(wb_sources)}")
        print(f"Number of WB indicators: {len(wb_indicators)}")
        
    if test_imf_client:
        
        imf_indicators = gdi.imf.indicators()
        imf_countries = gdi.imf.economies()
        
        imf_groups = gdi.imf.groups()
        imf_regions = gdi.imf.regions()
        
        imf_data = gdi.imf.data()
        
        
        print(f"Number of IMF countries: {len(imf_countries)}")
        print(f"Number of IMF groups: {len(imf_groups)}")
        print(f"Number of IMF regions: {len(imf_regions)}")
        print(f"Number of IMF indicators: {len(imf_indicators)}")
        
    if test_wto_client:
        
        wto_indicators = gdi.wto.indicators()
        wto_economies = gdi.wto.economies()
        
        wto_economic_groups = gdi.wto.economic_groups()
        wto_geographical_regions = gdi.wto.geographical_regions()
        wto_topics = gdi.wto.topics()
        wto_indicator_catagories = gdi.wto.indicator_catagories()
        wto_products_and_sectors = gdi.wto.products_and_sectors()
        wto_units = gdi.wto.units()
        
        # data = gdi.wto.data()
        
    if test_global_interface:
        
        indicators = gdi.indicators()
        economies = gdi.economies()
        for i in economies:
            print(i)
        print(len(economies))
        
    sys.exit()
