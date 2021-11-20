import os
from vyper import compile_code
from time import sleep
from web3 import Web3
from web3.eth import Eth
from utils.signer_eth import EthSigner

class ContractWrapper:
    w3 = None

    def __init__(self, contract_address: str, contract_path: str):
        self._get_w3()

        self.address = contract_address
        self.abi, self.bytecode = self._read_abi_and_bytecode(contract_path)

        self.contract = self.w3.eth.contract(Web3.toChecksumAddress(self.address), abi=self.abi)

    def _get_w3(self):
        if not (infura_uri:=os.environ.get("INFURA_URI")):
            raise EnvironmentError("Specify INFURA_URI environmental variable")
        self.w3 = Web3(Web3.HTTPProvider(infura_uri))
        self._test_connection
    
    def _test_connection(self):
        assert self.w3.isConnected(), "Connection to infura could not be established, check INFURA_URI env var"
    
    def _read_abi_and_bytecode(self, path_to_file):
        _tmp = self.read_contract_code(path_to_file, ["abi", "bytecode"])
        return _tmp["abi"], _tmp["bytecode"]

    def read_contract_code(self, path_to_file: str, *args):
        with open(path_to_file, "r") as f:
            return compile_code(f.read(), *args)

class EthNft(ContractWrapper):
    def __init__(self, 
        contract_address: str, 
        contract_path: str = os.path.join('eth_components', 'contracts', 'erc_721.vy')
    ):
        super().__init__(contract_address, contract_path)

    def get_name(self):
        return self.contract.functions.name().call()

    def get_symbol(self):
        return self.contract.functions.symbol().call()

    def get_token_uri(self, token_id: int):
        return self.contract.functions.tokenURI(token_id).call()

    def call_mint(self, token_id: int, token_uri: str, eth_signer: EthSigner) -> str:
        tx = self.contract.functions.mint(
            Web3.toChecksumAddress(eth_signer.public_key),
            token_id,
            token_uri
        ).buildTransaction({
            "nonce": Eth(self.w3).getTransactionCount(eth_signer.public_key),
            "from": eth_signer.public_key,
        }) 

        signed_tx = eth_signer.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction) 
        return tx_hash

    def call_approve(self, approved_address, token_id: int, eth_signer: EthSigner) -> str:
        tx = self.contract.functions.approve(
            Web3.toChecksumAddress(approved_address),
            token_id,
        ).buildTransaction({
            "nonce": Eth(self.w3).getTransactionCount(eth_signer.public_key),
            "from": eth_signer.public_key,
        }) 

        signed_tx = eth_signer.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction) 
        return tx_hash

class EthBridge(ContractWrapper):
    def __init__(self, 
        contract_address: str, 
        contract_path: str = os.path.join('eth_components', 'contracts', 'bridge.vy')
    ):
        super().__init__(contract_address, contract_path)

    def get_order_sign_hash(self, requester_address: str, nft_contract_address: str, token_id: int) -> str:
        return "0x" + self.contract.functions.get_order_sign_hash(
            Web3.toChecksumAddress(requester_address),
            Web3.toChecksumAddress(nft_contract_address),
            token_id, 
            True
        ).call().hex()

    def get_unmigrate_sign_hash(self, target_owner: str, nft_contract_address: str, token_id: int) -> str:
        return "0x" + self.contract.functions.get_unmigrate_sign_hash(
            Web3.toChecksumAddress(target_owner),
            Web3.toChecksumAddress(nft_contract_address),
            token_id
        ).call().hex()
    
    def subscribe_to_orders(self, *args):
        for event in self.contract.events.Order.getLogs():
            self.get_order_metadata(event, *args)
            
    def get_order_metadata(self):
        orders = []
        for event in self.contract.events.Order.getLogs():
            orders.append({
                "metadata_eth":{
                    "token_id": event.args.token_id,
                    "token_address": event.args.token_address,
                    "requester_address": event.args.requester_address,
                    "target_address": event.args.target_address
                }
            })
        return orders

    def call_order_migration(self, nft_contract_address: str, token_id: int, target_account: str, eth_signer: EthSigner) -> str:
        tx = self.contract.functions.order_migration(
            Web3.toChecksumAddress(nft_contract_address),
            token_id,
            bytes.fromhex(target_account.removeprefix('0x'))
        ).buildTransaction({
            "nonce": Eth(self.w3).getTransactionCount(eth_signer.public_key),
            "from": eth_signer.public_key,
        }) 

        signed_tx = eth_signer.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction) 
        return tx_hash

    def call_execute_migration(self, original_owner: str, nft_contract_address: str, token_id: int, signatures: str, eth_signer: EthSigner) -> str:
        tx = self.contract.functions.execute_migration(
            Web3.toChecksumAddress(original_owner),
            Web3.toChecksumAddress(nft_contract_address),
            token_id,
            bytes.fromhex(signatures.removeprefix('0x'))
        ).buildTransaction({
            "nonce": Eth(self.w3).getTransactionCount(eth_signer.public_key),
            "from": eth_signer.public_key,
        }) 

        signed_tx = eth_signer.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction) 
        return tx_hash

    def call_unmigrate_token(self, target_owner: str, nft_contract_address: str, token_id: int, signatures: str, eth_signer: EthSigner) -> str:
        tx = self.contract.functions.unmigrate_token(
            Web3.toChecksumAddress(target_owner),
            Web3.toChecksumAddress(nft_contract_address),
            token_id,
            bytes.fromhex(signatures.removeprefix('0x'))
        ).buildTransaction({
            "nonce": Eth(self.w3).getTransactionCount(eth_signer.public_key),
            "from": eth_signer.public_key,
        }) 

        signed_tx = eth_signer.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction) 
        return tx_hash