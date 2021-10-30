# from web3.auto import w3
import web3
from eth_utils import keccak

with open("keys/keyfile2.key", "r") as f: 
    private_key = bytes.fromhex(f.read())
message = bytes.fromhex("5bf1e3244d63b4a4126a055fdd1c046bc464b657d1f24c29dcb56d4a7d0b48ec")
account = web3.eth.Account.privateKeyToAccount(private_key)
# address = account.address
# message = keccak(bytes(address, 'utf-8'))

signature = account.signHash(message)

print(f"""
    message_raw= {message.hex()}
    message= {signature.messageHash.hex()}
    signature= {signature.signature.hex()}
    ----------------------------------------------------
""")

print(f"""
    r= {hex(signature.r)}
    s= {hex(signature.s)}
    v= {hex(signature.v)}
""")
print(len(message.hex()), message.hex())
print(len(signature.messageHash.hex()), signature.messageHash.hex())

# message_bytes = bytes.fromhex(message)
# signature_bytes = bytes.fromhex(signature.signature)

recovered_hash = web3.eth.Account.recoverHash(message, signature=signature.signature)
print(recovered_hash)