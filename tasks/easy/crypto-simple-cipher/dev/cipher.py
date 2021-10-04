#!/usr/bin/env python3

import os


def encrypt(key: bytes, plaintext: bytes) -> bytes:
    ciphertext = []

    for i in range(len(plaintext)):
        byte = plaintext[i]

        for j in range(len(key)):
            byte = ((byte ^ i) ^ (key[j] + j)) ^ (i * j)

        ciphertext.append(byte & 0xFF)

    return bytes(ciphertext)


def decrypt(key: bytes, ciphertext: bytes) -> bytes:
    raise NotImplementedError


def main():
    key = os.urandom(16)

    with open('flag.txt', 'rb') as file:
        flag = file.read().strip()

    ciphertext = encrypt(key, flag)
    print(ciphertext.hex())

    return


if __name__ == '__main__':
    main()
