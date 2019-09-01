from app_utils import public_enc_rsa


class CodefAccount(object):
    def __init__(self, public_key):
        self.public_key = public_key
        self.account_body = {
            'accountList': []
        }

    def get_account_body(self):
        """
        계정 생성에 필요한 body를 리턴한다
        :return: request시 필요한 body
        """
        return self.account_body

    def append_account_info(self, business_type
                                , organization_code
                                , password
                                , der_file
                                , key_file
                                , country_code='KR'
                                , client_type='P'
                                , login_type='0'):
        """
        connected_id를 발급받기 위한 정보를 추가한다

        :param business_type: 비지니스 코드
        :param organization_code: 기관 코드
        :param password: 앤드유저의 인증서 비밀번호
        :param der_file: 앤드유저의 인증서 DerFile
        :param key_file: 앤드유저의 인증서 KeyFile
        :param country_code: 국가코드
        :param client_type: 고객구분
        :param login_type: 로그인 타입
        """
        self.account_body['accountList'].append({
            'countryCode': business_type,
            'organization': organization_code,
            'password': public_enc_rsa(self.public_key, password),
            'derFile': der_file,
            'keyFile': key_file,
            'countryCode': country_code,
            'clientType': client_type,
            'login_type': login_type
        })


