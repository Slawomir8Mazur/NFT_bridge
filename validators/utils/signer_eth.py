import os
from typing import Optional
from web3.eth import Account

class EthSigner:
    def __init__(self, key_path: Optional[str]=None):
        if key_path:
            self.private_key: bytes = self.load_private_key_from_file(key_path)
        else:
            self.private_key: bytes = self.load_private_key_from_env_var()
        self.account: Account = Account.privateKeyToAccount(self.private_key)
        self.public_key: str = self.account.address

    @staticmethod
    def load_private_key_from_file(keyfile_path):
        with open(keyfile_path, "r") as f: 
            return bytes.fromhex(f.read())
    
    @staticmethod
    def load_private_key_from_env_var():
        if not (pk_string := os.environ.get("ETHEREUM_PRIVATE_KEY")):
            raise EnvironmentError("Set ETHEREUM_PRIVATE_KEY environment variable")
        try:
            pk_string = pk_string.removeprefix('0x')
            return bytes.fromhex(pk_string)
        except:
            raise EnvironmentError("Provided private key at ETHEREUM_PRIVATE_KEY was not valid hex string")

    def sign_hash(self, message: bytes):
        return "0x" + bytes(self.account.signHash(message).signature).hex()

    def sign_transaction(self, transaction):
        return self.account.sign_transaction(transaction)

    @staticmethod
    def get_signer(message: str, signature: str, validate=False) -> str:
        try:
            return Account.recoverHash(
                bytes.fromhex(message.removeprefix("0x")), 
                signature=bytes.fromhex(signature.removeprefix("0x"))
            )
        except:
            assert not validate, ValueError("Failed to calculate signer")
            return ""

    @staticmethod
    def concat_signatures(signatures: list[str]):
        return "0x" + "".join([
            s.removeprefix("0x") for s in signatures
        ])
