import sys
import requests
import json
import urllib
import logging
from codef_account import CodefAccount
from app_utils import string_b64encode, request_codef_api
from errors import TokenGenerateError


_GEN_TOKEN_URL = 'https://oauth.codef.io/oauth/token'
_GET_ACCOUNT_LIST = 'https://api.codef.io/v1/kr/bank/p/account/account-list'
_GET_CID_URL = 'https://api.codef.io/v1/account/create'


class CodefApi(object):
    def __init__(self, public_key, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.account = CodefAccount(public_key)

    def get_token(self):
        response_oauth = gen_token(_GEN_TOKEN_URL, self.client_id, self.client_secret)
        if response_oauth.status_code == 200:
            text_dict = json.loads(response_oauth.text)
            # reissue_token
            api_token = text_dict['access_token']
            return api_token
        else:
            print(response_oauth)
            print(response_oauth.status_code)
            raise TokenGenerateError('토큰 발급에 실패했습니다.')

    def request_api(self, api_url, token, body):
        """
        API 요청

        :param api_url: 요청 URL
        :param token: 식별 토큰
        :param body: body data
        :return:
        """
        return request_codef_api(api_url, token, body)


def gen_token(url, client_id, client_secret):
    auth_header = string_b64encode(client_id + ':' + client_secret, 'utf-8').decode("utf-8")

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + auth_header
    }

    response = requests.post(url, headers=headers, data='grant_type=client_credentials&scope=read')

    logging.debug(response.status_code)
    logging.debug(response.text)

    return response

