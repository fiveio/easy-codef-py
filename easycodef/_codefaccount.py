import json
import logging
import requests
from helper import public_enc_rsa, string_b64encode
from errors import TokenGenerateError


class CodefAccount(object):
    """
    CODEF Account 관련 요청을 핸들링 하기 위한 객체
    EasyCodef의 필드 값으로 셋팅됨
    """
    def __init__(self):
        pass

    @classmethod
    def gen_account_req_body(cls, **kwargs):
        """
        account API 요청에 필요한 body 데이터 생성

        :param: kwargs: connected_id | account_list
        :return: request body data
        """
        body = {}
        if 'connected_id' in kwargs:
            body['connectedId'] = kwargs['connected_id']
        if 'account_list' in kwargs:
            body['accountList'] = kwargs['account_list']

        return body

    @classmethod
    def gen_account_info(cls,
                         public_key,
                         business_type,
                         organization_code,
                         password,
                         der_file,
                         key_file,
                         country_code='KR',
                         client_type='P',
                         login_type='0'):
        """
        connected_id를 발급받기계정 추가 또는 수정시 필요한 account 데이터 생성

        :param public_key: 유저 퍼블릭키.
        :param business_type: 비지니스 코드.
        :param organization_code: 기관 코드.
        :param password: 앤드유저의 인증서 비밀번호. RSA 암호화 되어 셋팅됨.
        :param der_file: 앤드유저의 인증서 DerFile. base64 encoding된 string 타입 데이터.
                            helper의 file_to_base64활용을 권장함
        :param key_file: 앤드유저의 인증서 KeyFile. base64 encoding된 string 타입 데이터.
                            helper의 file_to_base64활용을 권장함
        :param country_code: 국가코드
        :param client_type: 고객구분
        :param login_type: 로그인 타입
        """
        return {
            'businessType': business_type,
            'organization': organization_code,
            'password': public_enc_rsa(public_key, password),
            'derFile': der_file,
            'keyFile': key_file,
            'countryCode': country_code,
            'clientType': client_type,
            'loginType': login_type
        }

    @classmethod
    def gen_access_token(cls, client_id, client_secret):
        """
        CODEF 사용을 위한 access_token 생성

        :param: client_id: 사용자 client_id
        :param: client_secret: 사용자 client_secret
        :return: access_token: CODEF API 사용을 위한 access_token
        :except: TokenGenerateError: 토큰 생성 실패
        """
        gen_token_url = 'https://oauth.codef.io/oauth/token'
        response = _request_gen_token(gen_token_url, client_id, client_secret)
        if response.status_code == 200:
            text_dict = json.loads(response.text)
            # reissue_token
            access_token = text_dict['access_token']
            return access_token
        else:
            message = f'\n response status = {response.status_code} \n access_token 생성이 실패했습니다.'
            raise TokenGenerateError(message)


def _request_gen_token(url, client_id, client_secret):
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

