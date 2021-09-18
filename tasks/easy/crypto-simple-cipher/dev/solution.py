#!/usr/bin/env python3

import string


def xor_ij(i: int, key_length: int) -> int:
    byte = 0

    for j in range(key_length):
        byte = (byte ^ i) ^ (i * j)

    return byte


def is_printable(text: bytes):
    return all(chr(byte) in string.printable for byte in text)


def main():
    key_length = 16

    with open('output.txt', 'r') as file:
        output = file.read().strip()
        ciphertext = bytes.fromhex(output)

    for key in range(256):
        plaintext = []

        for i in range(len(ciphertext)):
            byte = xor_ij(i, key_length) ^ (ciphertext[i] ^ key)
            plaintext.append(byte & 0xFF)

        flag_candidate = bytes(plaintext)

        if is_printable(flag_candidate):
            print(key, flag_candidate)

    return


if __name__ == '__main__':
    main()
