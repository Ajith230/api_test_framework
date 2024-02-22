from enum import Enum
from typing import Optional
from urllib.parse import urlparse

import requests

from framework.response import APIResponse


class RequestMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Driver:
    __API_URL = None

    @staticmethod
    def get_api_url():
        """
        Method to get the API URL.

        Returns:
            str: The API URL.

        Raises:
            ValueError: If the API URL is not set.
        """
        if Driver.__API_URL is None:
            raise ValueError("API URL not set")
        else:
            return Driver.__API_URL

    def __init__(self, url):
        """
            Initializes the class with the provided API url.

            Args:
            url (str): The API url to be set.
            """
        if Driver.__API_URL is None:
            self.set_api_url(url)
        self.__last_response: Optional[APIResponse] = None

    @property
    def response(self):
        if self.__last_response is None:
            raise ValueError("No response received yet, are you sure you have made a request?")
        return self.__last_response

    @staticmethod
    def set_api_url(url):
        """
        Set the API URL for the Driver class.

        Args:
            url (str): The URL to be set for the API.

        Raises:
            ValueError: If the provided URL is invalid.
        """
        # Check if the provided URL is valid
        if not Driver.__is_valid_url(url):
            raise ValueError(f"Invalid URL {url}")

        # Set the API URL
        Driver.__API_URL = url

    @staticmethod
    def __is_valid_url(url) -> bool:
        """
        Check if the given URL is valid.

        Args:
            url (str): The URL to be validated.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @staticmethod
    def __get_url_path(base_url: str, path: str):
        """
        Set the URL path by combining the base URL and the provided path.

        Args:
            base_url (str): The base URL.
            path (str): The path to be appended to the base URL.

        Returns:
            str: The combined URL path.

        Raises:
            AssertionError: If the resulting URL is invalid.
        """
        if 'http' in path or 'www' in path:
            return base_url
        if path.startswith(base_url):
            Driver.__is_valid_url(path)
            return path
        path = path[1:] if path.startswith("/") else path
        if base_url.endswith("/"):
            url = base_url + path
        else:
            url = base_url + "/" + path
        if Driver.__is_valid_url(url):
            return url
        else:
            assert False, f"Invalid URL {url}"

    def get(self, relative_path, headers=None, auth=None):
        """
        A static method to make a GET request with the given relative path, headers, and authentication.
        """
        method = RequestMethods.GET.value
        url = Driver.__get_url_path(Driver.get_api_url(), relative_path)
        print(url)
        return self.request(method=method, url=url, headers=headers, auth=auth)

    def post(self, relative_path, headers=None, auth=None, json=None):
        """
        Send a POST request to the specified relative path with optional headers, authentication, and JSON data.
        """
        method = RequestMethods.POST.value
        url = Driver.__get_url_path(Driver.get_api_url(), relative_path)
        return self.request(method=method, url=url, headers=headers, auth=auth, json=json)

    def put(self, relative_path, headers=None, auth=None, json=None):
        """
        Sends a PUT request to the specified `relative_path` with optional `headers`, `auth`, and `json` data.
        Returns the __response from the request.
        """
        method = RequestMethods.PUT.value
        url = Driver.__get_url_path(Driver.get_api_url(), relative_path)
        return self.request(method=method, url=url, headers=headers, auth=auth, json=json)

    def delete(self, relative_path, headers=None, auth=None, json=None):
        """
        Deletes a resource at the specified relative path using the DELETE method.

        :param relative_path: The relative path of the resource to delete.
        :param headers: (optional) A dictionary of headers to send with the request.
        :param auth: (optional) Authentication information for the request.
        :param json: (optional) A JSON object to send in the body of the request.

        :return: The __response from the DELETE request.
        """
        method = RequestMethods.DELETE.value
        url = Driver.__get_url_path(Driver.get_api_url(), relative_path)
        return self.request(method=method, url=url, headers=headers, auth=auth, json=json)

    def patch(self, relative_path, headers=None, auth=None, json=None):
        """
        Perform a PATCH request to the specified relative path with optional headers, authentication, and JSON data.
        """
        method = RequestMethods.PATCH.value
        url = Driver.__get_url_path(Driver.get_api_url(), relative_path)
        return self.request(method=method, url=url, headers=headers, auth=auth, json=json)

    def request(self, method, url, headers=None, auth=None, json=None) -> requests.Response:
        """
        A static method to make a request using the provided method, URL, headers, authentication, and JSON data.
        Parameters:
            method (str): The HTTP request method (e.g., 'GET', 'POST').
            url (str): The URL for the request.
            headers (dict, optional): The headers for the request.
            auth (tuple, optional): The authentication credentials (username, password) for the request.
            json (dict, optional): The JSON data to be sent in the request body.
        Returns:
            requests.Response: The __response from the HTTP request.
        """
        print(url)
        response = requests.request(method=method, url=url, headers=headers, auth=auth, json=json)
        self.__last_response = APIResponse(response)
        print(self.__last_response.raw_response)
        print(response.text)
        return response
