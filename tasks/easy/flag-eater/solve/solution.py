#!/usr/bin/env python3
from Crypto.Cipher import ARC4
from binascii import unhexlify

key = b'pancakes_berries_chocolate_milk_waffles_cupcakes_croissants' # from binary
data = unhexlify("24957FFCD5CD6CE6AD343B5132D1E8A5B228DC2EABFDECA89A8A4078210D0D616210732A0D766D") # from binary

ctx = ARC4.new(key)
print(ctx.decrypt(data))