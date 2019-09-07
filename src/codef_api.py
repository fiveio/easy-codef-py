import requests
import json
import logging
from codef_account import CodefAccount
from app_utils import string_b64encode, request_codef_api
from errors import TokenGenerateError


class CodefApi(object):

    def __init__(self):
        self.account = CodefAccount()
        pass

    def use_api(self, api_url, access_token, body):
        """
        API 요청

        :param api_url: 요청 URL
        :param body: body data
        :return: reponse data
        """
        return request_codef_api(api_url, access_token, body)

    def gen_access_token(self, client_id, client_secret):
        """
        CODEF 사용을 위한 access_token 생성

        :param: client_id: 사용자 client_id
        :param: client_secret: 사용자 client_secret
        :return: access_token: CODEF API 사용을 위한 access_token
        :except: TokenGenerateError: 토큰 생성 실패
        """
        gen_token_url = 'https://oauth.codef.io/oauth/token'
        response_oauth = request_gen_token(gen_token_url, client_id, client_secret)
        if response_oauth.status_code == 200:
            text_dict = json.loads(response_oauth.text)
            # reissue_token
            access_token = text_dict['access_token']
            return access_token
        else:
            raise TokenGenerateError(f'response status = {response_oauth.status_code}'
                                     , 'access_token 생성이 실패했습니다.')


def request_gen_token(url, client_id, client_secret):
    """
    토큰 생성 request 요청

    :param url: token 생성 API url
    :param client_id: 사용자 client_id
    :param client_secret: 사용자 client_secret
    :return:
    """
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

