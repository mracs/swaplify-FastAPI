import base64
import uuid
import json
import hashlib
from ast import literal_eval


def conv_to_json(raw):
    return json.dumps(literal_eval(raw))


def compute_hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def encode_base64(string):
    return base64.b64encode(string.encode()).decode()


def decode_base64(string):
    return base64.b64decode(string.encode()).decode()


def get_token(string):
    return uuid.UUID(compute_hash(string))


def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = uuid.UUID(uuid_to_test)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
