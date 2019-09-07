import json
from app_utils import public_enc_rsa, request_codef_api, url_unquote
from errors import ConnectedIdGenerateError


class CodefAccount(object):
    """
    CODEF API 사용을 위한
    """
    def __init__(self):
        pass

    def gen_account_req_body(self, **kwargs):
        body = {}
        if 'connected_id' in kwargs:
            body['connectedId'] = kwargs['connected_id']
        if 'account_list' in kwargs:
            body['accountList'] = kwargs['account_list']

        return body

    def gen_account_info(self, public_key
                             , business_type
                             , organization_code
                             , password
                             , der_file
                             , key_file
                             , country_code='KR'
                             , client_type='P'
                             , login_type='0'):
        """
        connected_id를 발급받기계정 추가 또는 수정시 필요한 account 데이터 생성

        :param public_key: 유저 퍼블릭키
        :param business_type: 비지니스 코드
        :param organization_code: 기관 코드
        :param password: 앤드유저의 인증서 비밀번호
        :param der_file: 앤드유저의 인증서 DerFile
        :param key_file: 앤드유저의 인증서 KeyFile
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

    def gen_connected_id(self, access_token, body):
        """
        connected id 생성 요청

        :param: access_token: user access_token
        :param: body: request body
                     gen_account_info와 gen_account_req_body 함수를 통해 생성할 수 있다.
        :return: connected_id, response_data:
                    connected_id: 유저 Connected Id
                    response_data: 파싱한 response body 데이터
        :raise: ConnectedIdGenerateError:
                    토큰 생성 실패 에러
        """
        codef_account_create_url = 'https://api.codef.io/v1/account/create'
        response = request_codef_api(codef_account_create_url, access_token, body)

        if response.status_code == 200:
            quoted_text = url_unquote(response.text)
            response_data = json.loads(quoted_text)
            connected_id = response_data['data']['connectedId']

            return connected_id, response_data
        else:
            raise ConnectedIdGenerateError(f'response status = {response.status_code}'
                                            , 'Connected Id 발급이 실패했습니다.')
