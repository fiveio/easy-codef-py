from codef_api import CodefApi
from app_utils import file_to_base64
from dev_config import public_key, client_id, client_secret

# public_key = ''
# client_id = ''
# client_secret = ''
der_file_path = '../npki/signCert.der'
key_file_path = '../npki/signPri.key'
api = CodefApi()

# 토큰 생성
access_token = api.account.gen_access_token(client_id, client_secret)

# api 요청을 위한 body 생성
account_list = list()
account_list.append(api.account.gen_account_info(public_key=public_key
                                               , business_type='BK'
                                               , organization_code='0004'
                                               , password=''
                                               , der_file=file_to_base64(der_file_path)
                                               , key_file=file_to_base64(key_file_path)))
body = api.account.gen_account_req_body(account_list=account_list)

# connected_id 발급
connected_id, response_data = api.account.gen_connected_id(access_token, body)
request_body = {
    'connectedId': connected_id,
    'organization': '0004'
}

# 개인 보유계좌 조회 exam
bank_api_url = 'https://tapi.codef.io/v2/kr/bank/p/account/account-list'
bank_data, status = api.use(bank_api_url, access_token, request_body)

print(bank_data)
print(status)
