#!/usr/bin/env python3

import io
import re
import ast
import tarfile

from Crypto.Util import Padding
from Crypto.Cipher import AES

import gmpy2


e = 3
bits = 1024
key_size = AES.key_size[0]


def decrypt_text(encrypted_text: bytes, encrypted_aes_key: bytes) -> bytes:
    aes_key_ciphertext = int.from_bytes(encrypted_aes_key, 'big')
    aes_key_plaintext = int(gmpy2.iroot(aes_key_ciphertext, e)[0]) 

    length = (aes_key_plaintext.bit_length() + 7) // 8
    aes_key = aes_key_plaintext.to_bytes(length, 'big')

    iv, encrypted_text = encrypted_text[:AES.block_size], encrypted_text[AES.block_size:]
    cipher = AES.new(key=aes_key, iv=iv, mode=AES.MODE_CBC)

    return Padding.unpad(cipher.decrypt(encrypted_text), AES.block_size)


def extract_archive(text: str) -> bytes:
    bits = {
        '  ': '1',
        ' ': '0'
    }

    delimiters = re.findall(r'(\s\s?)', text)
    payload = [bits[delimiter] for delimiter in delimiters]
    archive = int(''.join(payload), 2).to_bytes(len(payload) // 8, 'big')

    return archive


def extract_output(archive: bytes) -> bytes:
    filename = 'output.txt'

    with io.BytesIO(archive) as file:
        with tarfile.open(mode='r', fileobj=file) as tar:
            with tar.extractfile(filename) as output:
                return output.read()


def main():
    with open('book.txt', 'r') as file:
        book = file.read().strip()

    archive = extract_archive(book)
    print(archive)

    output = extract_output(archive)
    print(output)
    
    obj = ast.literal_eval(output.decode())

    encrypted_text = bytes.fromhex(obj['encrypted_text'])
    encrypted_aes_key = bytes.fromhex(obj['encrypted_aes_key'])

    text = decrypt_text(encrypted_text, encrypted_aes_key)
    print(text)


if __name__ == '__main__':
    main()
