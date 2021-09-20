#!/usr/bin/env python3

import os

from Crypto.Util import Padding
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


def aes_encrypt(key: bytes, data: bytes) -> bytes:
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)

    return cipher.encrypt(Padding.pad(data, AES.block_size))


def rsa_encrypt(key: RSA.RsaKey, data: bytes) -> bytes:
    plaintext = int.from_bytes(data, 'big')
    ciphertext = pow(plaintext, key.e, key.n)

    return ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, 'big')


def main():
    aes_key = os.urandom(AES.key_size[0])
    rsa_key = RSA.generate(bits=1024, e=3)

    with open('flag.txt', 'r') as file:
        flag = file.read().strip()

    text = f'Good job! Here is your flag: {flag}'.encode()

    encrypted_text = aes_encrypt(aes_key, text)
    encrypted_aes_key = rsa_encrypt(rsa_key, aes_key)

    obj = {
        'encrypted_text': encrypted_text.hex(),
        'encrypted_aes_key': encrypted_aes_key.hex()
    }

    with open('output.txt', 'w') as file:
        file.write(f'{obj}{os.linesep}')

    return


if __name__ == '__main__':
    main()
