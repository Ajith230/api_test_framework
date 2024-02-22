from requests import Response


class APIResponse:
    def __init__(self, response: Response):
        self.__response: Response = response

    @property
    def status_code(self):
        return self.__response.status_code

    @property
    def text(self):
        return self.__response.text

    def json(self):
        return self.__response.json()

    @property
    def raw_response(self):
        return self.__response

    def json_response(self):
        try:
            json = self.__response.json()
            if len(json) > 0:
                return json
            return self.__response
        except Exception:
            return ''

    def assert_status_code(self, status_code, assert_false_message=None):
        if assert_false_message is None:
            assert_false_message = self.json_response()
        assert self.status_code == status_code, assert_false_message

    def assert_status_code_200(self, assert_false_message=None):
        self.assert_status_code(status_code=200, assert_false_message=assert_false_message)

    def assert_status_code_400(self, assert_false_message=None):
        self.assert_status_code(status_code=400, assert_false_message=assert_false_message)

    def assert_status_code_500(self, assert_false_message=None):
        self.assert_status_code(status_code=500, assert_false_message=assert_false_message)

    def assert_status_code_404(self, assert_false_message=None):
        self.assert_status_code(status_code=404, assert_false_message=assert_false_message)

    def assert_is_success_status_codes(self, assert_false_message=None):
        is_success_status_code = 299 >= self.__response.status_code >= 200
        assert is_success_status_code, assert_false_message

    def assert_is_information_status_codes(self, assert_false_message=None):
        is_information_status_code = 199 >= self.__response.status_code >= 100
        assert is_information_status_code, assert_false_message

    def assert_is_redirect_status_codes(self, assert_false_message=None):
        is_redirect_status_code = 399 >= self.__response.status_code >= 300
        assert is_redirect_status_code, assert_false_message

    def assert_is_client_error_status_codes(self, assert_false_message=None):
        is_client_error_status_code = 499 >= self.__response.status_code >= 400
        assert is_client_error_status_code, assert_false_message

    def assert_is_server_error_status_codes(self, assert_false_message=None):
        is_server_error_status_code = 599 >= self.__response.status_code >= 500
        assert is_server_error_status_code, assert_false_message

    def assert_json_contains(self, key, value, assert_false_message=None):
        if assert_false_message is None:
            assert_false_message = self.json_response()
        assert key in self.__response.json(), assert_false_message
        assert self.__response.json()[key] == value, assert_false_message

    def assert_json_equals(self, value, assert_false_message=None):
        if assert_false_message is None:
            assert_false_message = self.json_response()
        assert self.__response.json() == value, assert_false_message

    def assert_text_contains(self, value, assert_false_message=None):
        if assert_false_message is None:
            assert_false_message = self.json_response()
        assert value in self.__response.text, assert_false_message
