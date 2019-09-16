import base64
import requests
import json
from urllib import parse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1
from typing import Union

def string_b64encode(text: str, enc_type: str) -> str:
    """
    문자열을 base64 encoding

    :param text: 인코딩할 문자열
    :param enc_type: 문자 인코딩 타입
    :return: base64로 인코딩된 문자열
    """
    return base64.b64encode(text.encode(enc_type)).decode('utf-8')


def b64str_decode(b64str: str, dec_type: str) -> str:
    """
    base64로 인코딩된 byte string을 decoding

    :param b64str: 인코딩된 bytes
    :param dec_type: 디코딩 타입
    :return: 디코딩된 문자열
    """
    return base64.b64decode(b64str.encode('utf-8')).decode(dec_type)


def public_enc_rsa(public_key: str, data: str) -> str:
    """
     RSA 암호화

    :param public_key: CODEF 회원에게 제공되는 PublicKey
    :param data: 암호화할 데이터
    :return: RSA256 암호화된 데이터
    """
    key_der = base64.b64decode(public_key)
    key_pub = RSA.import_key(key_der)
    cipher = PKCS1.new(key_pub)
    cipher_text = cipher.encrypt(data.encode())

    encrypted_data = base64.b64encode(cipher_text).decode('utf-8')

    return encrypted_data


def request_codef_api(api_url: str, token: str, body: dict) -> requests.models.Response:
    """
    코드에프 API 요청 유틸

    :param api_url: 요청 URL
    :param token: 코드에프 요청시 식별 토큰
    :param body: body data
    :return: response data
    """
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token
               }

    return requests.post(api_url, headers=headers, data=url_qoute(str(json.dumps(body))))


def file_to_base64(**kwargs: Union[str, bytes]) -> str:
    """
    파일을 byte string을 base64 encoding한 string data로 변환.
    \n
    file_path | file_data 중 한개 이상 필수 파라미터 필요.

    :param kwargs: file_path | file_data
                file_path: str
                file_data: bytes
    :return: 인코딩된 file string
    """
    if 'file_path' in kwargs:
        fp = open(kwargs['file_path'], 'rb')
        data = fp.read()
        fp.close()
        return base64.b64encode(data).decode('utf-8')
    elif 'file_data' in kwargs:
        return base64.b64encode(kwargs['file_data']).decode('utf-8')


def url_qoute(url: str) -> str:
    """
    urllib.parse.quote 사용
    :param url: url string
    :return:
    """
    return parse.quote(url)


def url_unquote(quote_url: str) -> str:
    """
    urllib.parse.unqoute_plus 사용
    :param quote_url: qoute url
    :return:
    """
    return parse.unquote_plus(quote_url)
