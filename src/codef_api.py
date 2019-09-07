import requests
import json
import logging
from codef_account import CodefAccount
from app_utils import string_b64encode, request_codef_api, url_unquote
from errors import TokenGenerateError, UseApiError


class CodefApi(object):

    def __init__(self):
        self.account = CodefAccount()
        pass

    def use(self, api_url, access_token, body):
        """
        API 요청

        :param api_url: 요청 URL
        :param body: body data
        :return: response data, response status
        """
        response = request_codef_api(api_url, access_token, body)

        quoted_text = url_unquote(response.text)
        response_data = json.loads(quoted_text)

        return response_data, response.status_code

