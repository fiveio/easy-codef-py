import json
from typing import Tuple
from ._codefaccount import CodefAccount
from .helper import request_codef_api, url_unquote


class EasyCodef(object):
    """
    CODEF API를 사용하기 위해 만들어 놓은 구현 클래스
    """
    def __init__(self):
        self.account = CodefAccount
        pass

    def req_api(cls, api_url: str, access_token: str, body: dict) -> Tuple[dict, int]:
        """
        API 요청

        :param api_url: 요청 URL
        :param access_token: access token
        :param body: request body
        :return: tuple[response data, response status]
                response data: dict result
                response status: response status
        """
        response = request_codef_api(api_url, access_token, body)

        quoted_text = url_unquote(response.text)
        response_data = json.loads(quoted_text)
        return response_data, response.status_code
