import base64
import requests
import urllib
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1

def string_b64encode(text, enc_type):
    """
    문자열을 base64 encoding

    :param text: 인코딩할 문자열
    :param enc_type: 문자 인코딩 타입
    :return: 인코딩된 bytes
    """
    if type(text) is not str:
       raise TypeError
    return base64.b64encode(text.encode(enc_type))


def b64str_decode(b64str, dec_type):
    """
    base64로 인코딩된 byte string을 decoding

    :param b64str: 인코딩된 bytes
    :param dec_type: 디코딩 타입
    :return: 디코딩된 문자열
    """
    if type(b64str) != 'bytes':
        raise TypeError
    return base64.b64decode(b64str).decode(dec_type)


def public_enc_rsa(public_key, data):
    """
     RSA 암호화

    :param public_key: CODEF 회원에게 제공되는 PublicKey
    :param data: 암호화할 데이터
    :return:
    """
    key_der = base64.b64decode(public_key)
    key_pub = RSA.importKey(key_der)
    cipher = PKCS1.new(key_pub)
    cipher_text = cipher.encrypt(data.encode())

    encrypted_data = base64.b64encode(cipher_text)

    return encrypted_data


def request_codef_api(api_url, token, body):
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

    return requests.post(api_url, headers=headers, data=urllib.parse.quote(str(json.dumps(body))))
