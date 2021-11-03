from web3.eth import Account

class EthSigner:
    def __init__(self, key_path):
        self.private_key: bytes = self.load_private_key_from_file(key_path)
        self.account: Account = Account.privateKeyToAccount(self.private_key)

    @staticmethod
    def load_private_key_from_file(keyfile_path):
        with open(keyfile_path, "r") as f: 
            return bytes.fromhex(f.read())

    def sign_hash(self, message: bytes):
        return self.account.signHash(message).signature

    @staticmethod
    def concat_signatures(signatures):
        return bytes.fromhex("".join([
        s.hex()[2:] for s in signatures
    ]))

    def broadcast(self):
        raise NotImplementedError
