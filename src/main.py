from codef_api import CodefApi
import json
from app_utils import url_unquote, file_to_base64
from dev_config import public_key, client_id, client_secret

# public_key = ''
# client_id = ''
# client_secret = ''
der_file_path = '../npki/signCert.der'
key_file_path = '../npki/signPri.key'
codef_api = CodefApi(public_key, client_id, client_secret)

# 토큰 생성
auth_token = codef_api.get_token()
account_list = []
account_list.append(codef_api.account.gen_account_info(business_type='BK'
                                                       , organization_code='0004'
                                                       , password=''
                                                       , der_file=file_to_base64(der_file_path)
                                                       , key_file=file_to_base64(key_file_path)))
body = codef_api.account.gen_account_body(account_list=account_list)

codef_account_create_url = 'https://api.codef.io/v1/account/create'
response = codef_api.request_api(codef_account_create_url, auth_token, body)

connected_id = None
if response.status_code == 200:
    quoted_text = url_unquote(response.text)
    dict_data = json.loads(quoted_text)
    connected_id = dict_data['data']['connectedId']
    print(dict_data)

api_body = {
    'connectedId': connected_id,
    'organization': '0004'
}
bank_api_url = 'https://api.codef.io/v1/kr/bank/p/account/account-list'
response = codef_api.request_api(bank_api_url, auth_token, api_body)
if response.status_code == 200:
    quoted_text = url_unquote(response.text)
    dict_data = json.loads(quoted_text)
    print(dict_data)

