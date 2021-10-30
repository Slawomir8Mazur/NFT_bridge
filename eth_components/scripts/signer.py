import ed25519
import os

sk,vk = ed25519.create_keypair(entropy=os.urandom)
print(sk, vk)

message = bytes.fromhex('D0a7efE60Fd0850FDc2A63795a4a55460e732f1c')
print(message)

signature = sk.sign(message)
# signature = sk.sign(message, prefix=, encoding=)

print(message.hex())
print(signature.hex())