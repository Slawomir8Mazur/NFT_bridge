import ed25519
import os

sk,vk = ed25519.create_keypair()
print(sk.to_bytes().hex(), vk.to_bytes().hex())

message = bytes.fromhex('5bf1e3244d63b4a4126a055fdd1c046bc464b657d1f24c29dcb56d4a7d0b48ec')

signature = sk.sign(message)
# signature = sk.sign(message, prefix=, encoding=)

print(len(message), message.hex())
print(len(signature), signature.hex())