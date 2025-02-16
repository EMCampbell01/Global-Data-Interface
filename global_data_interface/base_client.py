from abc import ABC, abstractmethod
from typing import List
from urllib.parse import urlencode, urljoin, urlparse, parse_qs
import requests


class APIError(Exception):
    """Custom exception for WTO API errors."""
    pass


class BaseClient(ABC):
    
    BaseUrl: str = ''
    
    def __init__(self, api: str, api_key = None, headers = None):
        self.api = api
        self.api_key = api_key
        self.headers = headers
        
    def _construct_url(self, url_base: str, path_segments: List[str], query_parameters: dict):
        url = self._add_path_segments(url_base, path_segments)
        url = self._add_query_parameters(url, query_parameters)
        return url
    
    @staticmethod
    def _add_path_segments(url_base: str, path_segments: List[str]):
        # Normalize the base URL by ensuring it ends with a slash
        if not url_base.endswith('/'):
            url_base += '/'

        # Concatenate all path segments
        url = url_base + '/'.join(path_segments)
        return url
    
    @staticmethod
    def _add_query_parameters(url: str, query_parameters: dict) -> str:
        """Adds query parameters to a URL, handling parameters safely.

        Args:
            url (str): The base URL or existing path.
            query_parameters (dict): Dict containing params and values.

        Returns:
            str: The updated URL with the new query parameters.
        """
        # Filter out parameters with None values
        filtered_params = {k: v for k, v in query_parameters.items() if v is not None}
        
        # Parse the existing URL to check for existing query parameters
        parsed_url = urlparse(url)
        existing_params = parse_qs(parsed_url.query)
        
        # Add the new parameters to the existing ones
        existing_params.update(filtered_params)
        
        # Rebuild the URL with the updated query string
        query_string = urlencode(existing_params, doseq=True)
        return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{query_string}"
    
    def _request(self, method: str, url: str, payload=None) -> requests.Response:
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response

        except requests.exceptions.Timeout:
            raise APIError(f"Request to {self.api} API timed out")
        except requests.exceptions.ConnectionError:
            raise APIError(f"Failed to connect to {self.api} API")
        except requests.exceptions.HTTPError as e:
            raise APIError(f"{self.api} API returned an HTTP error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            action = "getting" if method.upper() == "GET" else "posting"
            raise APIError(f"An error occurred while {action} data from {self.api} API: {e}")

    def _get(self, url: str) -> requests.Response:
        return self._request("GET", url)

    def _post(self, url: str, payload) -> requests.Response:
        return self._request("POST", url, payload)
    
    @abstractmethod
    def info(self) -> None:
        """
        Abstract method for retrieving API-specific information.
        
        This method must be implemented by any subclass of BaseClient.
        """
        pass