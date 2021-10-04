#!/usr/bin/env python3

import random
import loremipsum

# monkey patch
loremipsum._GENERATOR = loremipsum.Generator(
    loremipsum.generator._SAMPLE,
    list(map(bytes.decode, loremipsum.generator._DICTIONARY))
)


def main():
    delimiters = {
        '0': ' ',
        '1': '  '
    }

    with open('archive.tar.gz', 'rb') as file:
        archive = file.read()

    payload = bin(int.from_bytes(archive, 'big'))[2:]
    payload = '0' * ((8 - len(payload) % 8) % 8) + payload

    tokens = loremipsum.get_sentence(True).split(' ')

    while len(tokens) < len(payload):
        sentence = loremipsum.get_sentence(False)
        tokens.extend(sentence.split(' '))

    text = []

    for bit, token in zip(payload, tokens):
        text.extend([token, delimiters[bit]])

    text.extend([
        random.choice(loremipsum.generator._DICTIONARY).decode(),
        random.choice(loremipsum.generator._SENTENCE_DELIMITERS)
    ])

    with open('book.txt', 'w') as file:
        file.write(''.join(text))

    return


if __name__ == '__main__':
    main()
