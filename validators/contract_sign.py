import os
from web3 import Web3
from utils.contract_wrapper import ContractWrapper
from utils.signer import EthSigner

    
contract_wrapper = ContractWrapper(
    os.path.join('eth_components', 'contracts', 'main.py'), 
    "0x313309192D561C99563e8cEDcACd8a1655b73879"
)

# Load signers
signers = [EthSigner(os.path.join('keys', f'keyfile{i}.key')) for i in range(1,5)]

order_sign_hash = contract_wrapper.contract.functions.get_order_sign_hash(
    Web3.toChecksumAddress("0x291Eea42f2806d7b5f14C5e71f3a97b0a5Bcf62e"),
    Web3.toChecksumAddress("0x5036bf1c86b03dc74bcf490ea5fbad4426069069"),
    21, 
    True
).call()

# Prepare signature for the contract
signature = EthSigner.concat_signatures([
    s.sign_hash(order_sign_hash)
    for s in signers
])

print(signature.hex())