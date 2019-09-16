import json
import requests
from typing import Union
from .helper import public_enc_rsa, string_b64encode, file_to_base64
from .errors import TokenGenerateError


class CodefAccount(object):
    """
    CODEF Account 관련 요청을 핸들링 하기 위한 객체
    \n
    EasyCodef의 필드 값으로 셋팅됨
    """
    def __init__(self):
        pass

    @classmethod
    def gen_account_req_body(cls,
                             connected_id: str = None,
                             account_list: list = None) -> dict:
        """
        codef account관련 요청을 위한 request body 생성.

        :param connected_id: codef connected id
        :param account_list: account list
        :return: request body
        """
        body = {}
        if connected_id is None and account_list is None:
            raise AttributeError('At least one of connected_id and account_list must contain a parameter.')

        if connected_id is not None:
            body['connectedId'] = connected_id
        if account_list is not None:
            body['accountList'] = account_list

        return body

    @classmethod
    def gen_account_info(cls,
                         business_type: str,
                         organization_code: str,
                         password: str,
                         der_file: Union[str, bytes] = None,
                         key_file: Union[str, bytes] = None,
                         id: str = None,
                         country_code: str = 'KR',
                         client_type: str = 'P',
                         login_type: str = '0',
                         public_key: str = None,
                         birthday: str = None) -> dict:
        """
        connected_id를 발급받기계정 추가 또는 수정시 필요한 account 데이터 생성
        \n
        코드 값 https://developer.codef.io/ 참고

        :param der_file: 앤드유저의 인증서 DerFile.
            파일 경로(str) 또는 파일 데이터 (bytes)로 전달
        :param key_file: 앤드유저의 인증서 KeyFile. base64 encoding된 string 타입 데이터.
            파일 경로(str) 또는 파일 데이터 (bytes)로 전달
        :param id: login_type = '1'일 경우 인증 id
        :param business_type: 비지니스 코드.
        :param organization_code: 기관 코드.
        :param password: 앤드유저의 인증서 비밀번호.
                    codef 계정 public_key로 RSA256 암호화가 되어 있어야하며,
                    만약 평문일 경우 public_key를 파라미터 값으로 추가해주면
                    함수내에서 public_key값으로 암호화 한다.
        :param country_code: 국가코드
        :param client_type: 고객구분
        :param login_type: 로그인 타입
        :param public_key: codef 계정 public_key
        :param birthday: 생년월일(yymmdd)
        """
        body = {
            'businessType': business_type,
            'organization': organization_code,
            'password': password,
            'countryCode': country_code,
            'clientType': client_type,
            'loginType': login_type
        }

        if login_type is '0':
            if der_file is not None and key_file is not None:
                _set_auth_files_in_body(body, der_file, key_file)
            else:
                raise AttributeError('If login_type is 0, der_file and key_file are required parameters.')
        elif login_type is '1':
            if id is not None:
                body['id'] = id
            else:
                raise AttributeError('If login_type is 1, id are required parameter.')

        if public_key is not None:
            if password is None or password is '':
                raise AttributeError('If you include public_key, a password is required to apply RSA.')
            body['password'] = public_enc_rsa(public_key, body['password'])

        if birthday is not None:
            body['birthday'] = birthday

        return body

    @classmethod
    def gen_access_token(cls, client_id: str, client_secret: str) -> str:
        """
        CODEF 사용을 위한 access_token 생성

        :param client_id: codef 계정 API client_id
        :param client_secret: codef 계정 API client_secret

        :return: CODEF API 사용을 위한 access_token

        :except TokenGenerateError: 토큰 생성 실패
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


def _request_gen_token(url: str, client_id: str, client_secret: str) -> requests.models.Response:
    """
    토큰 생성 request 요청

    :param url: token 생성 API url
    :param client_id: 사용자 client_id
    :param client_secret: 사용자 client_secret

    :return: Response
    """
    auth_header = string_b64encode(client_id + ':' + client_secret, 'utf-8')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + auth_header
    }

    return requests.post(url, headers=headers, data='grant_type=client_credentials&scope=read')


def _set_auth_files_in_body(body: dict, der_file: Union[str, bytes], key_file: Union[str, bytes]) -> None:
    """
    요청 바디 데이터에 인증서 파일(der & key)값을 셋팅한다.

    :param body: request body
    :param der_file: der_file path(str) | der_file data(bytes)
    :param key_file: key_file path(str) | key_file data(bytes)
    """
    if type(der_file) is str:
        body['derFile'] = file_to_base64(file_path=der_file)
    elif type(der_file) is bytes:
        body['derFile'] = file_to_base64(file_data=der_file)
    else:
        raise TypeError('der_file accepts only file paths (str) or data (bytes).')

    if type(key_file) is str:
        body['keyFile'] = file_to_base64(file_path=key_file)
    elif type(key_file) is bytes:
        body['keyFile'] = file_to_base64(file_data=key_file)
    else:
        raise TypeError('key_file accepts only file paths (str) or data (bytes).')
