import configparser
import time

import jwt
import hashlib

config = configparser.ConfigParser()
config.read('environment.ini')
JWT_EXPIRE = 3600


def generate_jwt(account_id: str, secret_key: str, uri: str):
    """
    Returns a JWT to be used with Zephyr Squad api
    :param account_id:
    :param secret_key:
    :param uri:
    :return:
    """
    # zephyr_jwt = jwt.encode({ "context": { "user": { "accountId": account_id } } }, secret_key, algorithm="HS256")
    # config["zephyr.api"]["jwt"] = zephyr_jwt
    payload_token = {
        'sub': account_id,
        'qsh': hashlib.sha256(uri.encode('utf-8')).hexdigest(),
        'iss': secret_key,
        'exp': int(time.time()) + JWT_EXPIRE,
        'iat': int(time.time())
    }
    return jwt.encode(payload_token, secret_key, algorithm='HS256')
