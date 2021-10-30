# from web3.auto import w3
import web3
from eth_utils import keccak

private_key = "0x78d0030cb696f47a55b378505b8c3054b3f064054a2d0c7531771f71d008b2ca"

account = web3.eth.Account.privateKeyToAccount(private_key)
address = account.address
message = keccak(bytes(address, 'utf-8'))

signature = account.sign_message(address)

print(f"""
    message={hex(int(message, 16))}
    signature={hex(int(signature, 16))}
""")