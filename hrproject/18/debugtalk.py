import time

from httprunner import __version__

import random

import hashlib

import rsa

import base64

import json

import string



def get_httprunner_version():

    return __version__



def sum_two(m, n):

    return m + n



def sleep(n_secs):

    time.sleep(n_secs)



def get_timestamp():

    return str(int(time.time()*1000))



def get_param(jsonstr):

    k = json.dumps(jsonstr)

    key = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAsm9gD6L21qAJGWbU9ZSCdmppx96gECxKyKXluOtLhaTPf0hpJwcFd2fWJczM+YlRexYU1YVuPbq2oIQhqOBDdsD+y3S+kkXfObWe13mJjzoRrg3xDA5hWY9sMLwqZ7RFnNIGjz22VmI5xbEH311O3X4clvZz2ofGaVnYoHYQGMptRwuHvL7/MV5SVlBzxvw4XTig1muUql1321c3tLvuLHhmo+Q9rfUq0ef8lptxwOptvxgsAC5D71wlqOBrO4unspBZ6FNRBznB8sdSHZAWotpKCoCXztV+OdEH9EdlS84B+e1vJMRqCFmYjMcm5OZ7dcwKBs/LqSU4R3pq2gMxyy4Xp/+WAp9xiS7+bgWMnGrLeI01spXaVxYnB8Vc7D74xLPqISNYBpsAvEwA+bOKur5i4LS18A3ZBEvXXIGdz/XkylR5KGN2dTY725XRxDIBOVbyU0WJG4OsQNsMldddlwGWsopTg3R/4khNn/DrclN5GXSxlDVWWtgsMB3J0aneGNfPBJuVU0aoC1pDKA+YUzOlTRsgJJKAxn83+SlmAapkyw1AVqhoEeW6m0MosT8fVgT7b+cheupm1vZz5lRoxL/QKWVdlI8gYpzFeLLmore8pi1BUq4f1OK1feCleSqxlcgPn2/XtRxtH+jl3oP8HHCRIB8VnI31McBhjSHOoiECAwEAAQ=='

    key = base64.standard_b64decode(key)

    a = rsa.PublicKey.load_pkcs1_openssl_der(key)

    cipher_text = rsa.encrypt(k.encode('utf-8'),a)

    b = base64.b64encode(cipher_text)

    print("加密参数===================================================")

    print(jsonstr)

    print("加密后字符串============================================")

    print(bytes.decode(b))

    return bytes.decode(b)



def get_order_num():

    a = str(int(time.time()*1000))

    b = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    return b + '_' + a



def pre_request(request):

    p = request.get('req_json')

    print('请求参数打印========================================')

    print(p)

    p1 = get_param(p.get('encryption_params'))

    p['params'] = p1

    request['params'] = p #用content-type=application/x-www-form-urlencoded，方式请求


# def sleep_ns(n):

#     print('休息n秒',n)

#     time.sleep(n)