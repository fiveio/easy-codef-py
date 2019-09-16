# Easy Codef
[CODEF API](https://codef.io)를 통해 테스트 및 개발할 때 개발자가 인코딩, 암호화 등 API 요청에 필요한 전처리 작업을
최소화하는 것, 그리고 누구나 쉽게 개발할 수 있는 것을 지향합니다.

때문에 API 요청에 필요한 전처리 과정을 구현했습니다.

Easy Codef를 통해 누구나 쉽게 CODEF API를 사용할 수 있기를 바랍니다.

### Usage Guide
1. API 사용을 위한 CODEF 계정이 필요합니다.
2. CODEF API에 사용되는 요청 URL, 파리미터, 코드, 구동방식 등 CODEF API에 대한 자세한 정보는 [CODEF API Dev Guide](https://developer.codef.io)를 참고해주세요.
3. exam 폴더에 Easy Codef 사용 예제(CODEF Develop 버전 기준)가 있습니다.


### Python Version
python 3.x를 권장합니다.

### Setup
```bash
$ pip install easycodef
```

### Example
예제 코드는 [exam/exam.py](https://github.com/dc7303/easy-codef-py/blob/master/exam/exam.py)를 기반으로 작성되었습니다.

easycodef 인스턴스 생성 및 CODEF 사용에 필요한 access_token을 생성합니다. 
이때 client_id와 client_secret은 CODEF 계정 관리에서 **키관리**에서 확인할 수 있습니다.
```python
from easycodef import EasyCodef

api = EasyCodef()

access_token = api.account.gen_access_token(client_id='', client_secret='')
```
API 사용을 위한 엔드 유저의 계정 관련 요청에 필요한 request body 데이터를 생성합니다.

요청별 필요한 데이터 정보 또는 응답 정보는 [CODEF Dev Guide](https://developer.codef.io/docs/cert/account/create)에서 확인하세요.

gen_account_info의 파라미터 정보는 [여기](https://github.com/dc7303/easy-codef-py/blob/master/easycodef/_codefaccount.py#L40)에서
확인하세요. 아래 예제 코드는 국민은행(개인) connected_id 생성 예제입니다.
```python
account_list = list()
accout_info = api.account.gen_account_info(business_type='BK',
                                           organization_code='0004',
                                           password='',
                                           public_key='',
                                           der_file='파일 경로 또는 bytes',
                                           key_file='파일 경로 또는 bytes')
accout_info.append(accout_info)

body = api.account.gen_account_req_body(account_list=account_list)
```
easycodef에서 모든 API 요청은 [req_api](https://github.com/dc7303/easy-codef-py/blob/master/easycodef/easycodef.py#L15)를 사용합니다.
```python
codef_account_create_url = 'https://api.codef.io/v1/account/create'

response_data, response_status_code = api.req_api(codef_account_create_url, access_token, body)
```
생성된 connected id를 포함하여 데이터 조회 업무를 사용하기 위한 body 값을 만든 후 req_url로 요청합니다.
 
```python
request_body = {
    'connectedId': response_data['data']['connectedId'],
    # ...parameters
}
api_url = 'https://development.codef.io/v1/kr/bank/p/account/account-list'

bank_data, status = api.req_api(api_url, access_token, request_body)
```

### License
[LICENSE](https://github.com/dc7303/easy-codef-py/blob/master/LICENSE)

### Author
[Mark(margurt)](https://github.com/dc7303)