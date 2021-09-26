#!/usr/bin/env python3
import re

data = re.findall(b"write\(1, \".*\", 2\)", open("out.txt", 'rb').read())
for i in data:
    print(i[10:11].decode(), end='')
print("")