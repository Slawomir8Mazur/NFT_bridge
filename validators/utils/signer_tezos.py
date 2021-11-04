import os
from pytezos.crypto import Key

sk = Key.from_encoded_key('edsk3nM41ygNfSxVU4w1uAW3G9EnTQEB5rjojeZedLTGmiGRcierVv')
sk.public_key()

class TezSigner:
    def __init__(self, key_path=None):
        if key_path:
            self.private_key: Key = self.load_private_key_from_file(key_path)
        else:
            self.private_key: Key = self.load_private_key_from_env_var()
        self.public_key: str = self.private_key.public_key()

    @staticmethod
    def _load_private_key(private_key_string):
        return Key.from_encoded_key(private_key_string)

    @classmethod
    def load_private_key_from_file(cls, keyfile_path):
        with open(keyfile_path, "r") as f: 
            return cls._load_private_key(f.read())
    
    @classmethod
    def load_private_key_from_env_var(cls):
        if not (pk_string := os.environ.get("TEZOS_PRIVATE_KEY")):
            raise EnvironmentError("Set TEZOS_PRIVATE_KEY environment variable")
        return cls._load_private_key(pk_string)

    def sign_hash(self, message: bytes):
        return self.private_key.sign(message)

    def sign_transaction(self, transaction):
        raise NotImplementedError
