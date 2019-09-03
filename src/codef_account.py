from app_utils import public_enc_rsa


class CodefAccount(object):
    def __init__(self, public_key):
        self.public_key = public_key

    def gen_account_body(self, **kwargs):
        body = {}
        if 'connected_id' in kwargs:
            print(kwargs['connected_id'])
            body['connectedId'] = kwargs['connected_id']
        if 'account_list' in kwargs:
            body['accountList'] = kwargs['account_list']

        return body

    def gen_account_info(self, business_type
                             , organization_code
                             , password
                             , der_file
                             , key_file
                             , country_code='KR'
                             , client_type='P'
                             , login_type='0'):
        """
        connected_id를 발급받기계정 추가 또는 수정시 필요한 account 데이터 생성

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
            'password': public_enc_rsa(self.public_key, password),
            'derFile': der_file,
            'keyFile': key_file,
            'countryCode': country_code,
            'clientType': client_type,
            'loginType': login_type
        }


