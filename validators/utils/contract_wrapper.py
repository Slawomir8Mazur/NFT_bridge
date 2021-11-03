import os
from web3 import Web3
from vyper import compile_code

class ContractWrapper:
    w3 = None

    def __init__(self, contract_path: str, contract_address: str):
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
