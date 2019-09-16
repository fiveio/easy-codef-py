from easycodef import EasyCodef

# Easy Codef 생성
api = EasyCodef()

# codef에서 발급받은 client_id, client_secret
client_id = ''
client_secret = ''

# 인증서 file 경로 또는 data(bytes)
der_file = ''
key_file = ''

# 토큰 생성
access_token = api.account.gen_access_token(client_id, client_secret)

# api 요청을 위한 body 생성
account_list = list()
accout_info = api.account.gen_account_info(business_type='',
                                           organization_code='',
                                           password='',
                                           public_key='',
                                           der_file=der_file,
                                           key_file=key_file)
account_list.append(accout_info)
body = api.account.gen_account_req_body(account_list=account_list)

# connected_id 생성 요청
codef_account_create_url = 'https://api.codef.io/v1/account/create'

# connected_id 발급
response_data, response_status_code = api.req_api(codef_account_create_url, access_token, body)

request_body = {
    'connectedId': response_data['data']['connectedId'],
    # ...
}

# 개인 보유계좌 조회 exam
api_url = 'https://development.codef.io/v1/kr/bank/p/account/account-list'

bank_data, status = api.req_api(api_url, access_token, request_body)

