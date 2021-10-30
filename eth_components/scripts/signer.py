# from web3.auto import w3
import web3
# from eth_utils import keccak

with open("keys/keyfile2.key", "r") as f: 
    private_key = bytes.fromhex(f.read())
message = bytes.fromhex("5bf1e3244d63b4a4126a055fdd1c046bc464b657d1f24c29dcb56d4a7d0b48ec")

account = web3.eth.Account.privateKeyToAccount(private_key)
# address = account.address
# message = keccak(bytes(address, 'utf-8'))

signature = account.signHash(message)
recovered_address = web3.eth.Account.recoverHash(message, signature=signature.signature)

print(f"""
    message= {signature.messageHash.hex()}
    signature= {signature.signature.hex()}
    address= {recovered_address}
    ----------------------------------------------------
""")