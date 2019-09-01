from codef_api import CodefApi
import json
from app_utils import url_unquote

public_key = ''
client_id = ''
client_secret = ''

der_file = None
key_file = None

with open('../npki/signCert.der', 'rb') as file:
    der_file = file.read().hex()
with open('../npki/signPri.key', 'rb') as file:
    key_file = file.read().hex()


codef_api = CodefApi(public_key, client_id, client_secret)
# 토큰 생성
auth_token = codef_api.get_token()

account_list = []
account_list.append(codef_api.account.gen_account_info(business_type='BK'
                                                       , organization_code='0005'
                                                       , password=''
                                                       , der_file=der_file
                                                       , key_file=key_file))

body = codef_api.account.gen_account_body(account_list=account_list)

codef_account_create_url = 'https://api.codef.io/v1/account/create'
response = codef_api.request_api(codef_account_create_url, auth_token, body)

if response.status_code == 200:
    quoted_text = url_unquote(response.text)
    dict_data = json.loads(quoted_text)
    print(dict_data)
