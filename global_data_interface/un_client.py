from global_data_interface.base_client import BaseClient


class UNClient(BaseClient):
    '''A client for interacting with the IMF API.'''
    
    BASE_URL = 'https://www.imf.org/external/datamapper/api/v1'
    API_DOCS = 'https://www.imf.org/external/datamapper/api/help'

    def __init__(self):
        super().__init__('IMF')
        
    def info(self) -> None:
        print(f'''
              UN API CLIENT INFO:
              
              BASE URL: {self.BASE_URL}
              API DOCS: {self.API_DOCS}
              ''')