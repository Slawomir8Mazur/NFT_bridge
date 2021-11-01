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

def sign_single(message: bytes, keyfile_path: str):
    with open(keyfile_path, "r") as f: 
        private_key = bytes.fromhex(f.read())
    account = web3.eth.Account.privateKeyToAccount(private_key)
    signature = account.signHash(message)
    return signature

def concat_signatures(signatures):
    return "0x" + "".join([
        s.signature.hex()[2:] for s in signatures
    ])

def test_n1():
    """provide 2 signatures from 2 signers, test for to few signatures"""
    message = bytes.fromhex("5bf1e3244d63b4a4126a055fdd1c046bc464b657d1f24c29dcb56d4a7d0b48ec")
    signatures = [sign_single(message, f"keys/keyfile{i}.key") for i in range(1,3)]
    print(concat_signatures(signatures))

def test_n2():
    """provide 4 signatures from 2 signers, test for duplicates"""
    message = bytes.fromhex("5bf1e3244d63b4a4126a055fdd1c046bc464b657d1f24c29dcb56d4a7d0b48ec")
    signatures = [sign_single(message, f"keys/keyfile{i}.key") for i in range(1,3)]
    [signatures.append(i) for i in signatures.copy()]
    print(concat_signatures(signatures))

def test_p():
    message = bytes.fromhex("5bf1e3244d63b4a4126a055fdd1c046bc464b657d1f24c29dcb56d4a7d0b48ec")
    signatures = [sign_single(message, f"keys/keyfile{i}.key") for i in range(1,5)]
    print(concat_signatures(signatures))

test_p()
