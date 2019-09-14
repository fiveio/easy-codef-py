from easycodef import EasyCodef
from apputil import file_to_base64
from devconfig import public_key, client_id, client_secret


# public_key = ''
# client_id = ''
# client_secret = ''
der_file_path = '../npki/signCert.der'
key_file_path = '../npki/signPri.key'
api = EasyCodef()

# 토큰 생성
access_token = api.account.gen_access_token(client_id, client_secret)

# api 요청을 위한 body 생성
account_list = list()
account_list.append(api.account.gen_account_info(public_key=public_key,
                                                 business_type='BK',
                                                 organization_code='0004',
                                                 password='',
                                                 der_file=file_to_base64(der_file_path),
                                                 key_file=file_to_base64(key_file_path)))
body = api.account.gen_account_req_body(account_list=account_list)

# connected_id 생성 요청
codef_account_create_url = 'https://api.codef.io/v1/account/create'
# connected_id 발급
response_data = api.account.req_account_api(codef_account_create_url, access_token, body)
request_body = {
    'connectedId': response_data['data']['connectedId'],
    'organization': '0004'
}

# 개인 보유계좌 조회 exam
bank_api_url = 'https://development.codef.io/v1/kr/bank/p/account/account-list'
bank_data, status = api.use(bank_api_url, access_token, request_body)
