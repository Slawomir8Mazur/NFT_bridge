import os
from typing import Callable
from web3 import Web3
from vyper import compile_code
import asyncio

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

class EthBridge(ContractWrapper):
    def __init__(self, 
        contract_address: str = "0xe8750c0d2ead47451a11a19e15c1c12f195080ec", 
        contract_path: str = os.path.join('eth_components', 'contracts', 'main.py')
    ):
        super().__init__(contract_address, contract_path)
        self.pool_interval = 3

    def get_order_sign_hash(self, requester_address: str, nft_contract_address: str, token_id: int) -> str:
        return "0x" + self.contract.functions.get_order_sign_hash(
            Web3.toChecksumAddress(requester_address),
            Web3.toChecksumAddress(nft_contract_address),
            token_id, 
            True
        ).call().hex()

    def send_signed_order(self):
        raise NotImplementedError

    def pool_logs(self, subscribtion, *args):
        """
        >>> eth_bridge.pool_logs(eth_bridge.subscribe_to_orders, print)
        """
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(
                subscribtion(*args)
            ))
        finally:
            loop.close()

    async def subscribe_to_orders(self, *args):
        while True:
            for event in self.contract.events.Order.getLogs():
                self.get_order_metadata(event, *args)
            await asyncio.sleep(self.pool_interval)

    def get_order_metadata(self, order_event, *args: list[Callable]):
        order = {
            "metadata":{
                "token_id": order_event.args.token_id,
                "token_address": order_event.args.token_address,
                "requester_address": order_event.args.requester_address,
                "target_address": order_event.args.target_address.decode('utf-8')
            }
        }
        [f(order) for f in args]