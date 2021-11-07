import os
from web3 import Web3
from web3.eth import Eth
from utils.signer_eth import EthSigner
from utils.contract_wrapper import EthBridge

eth_signer = EthSigner("keys/keyfile2.key")
eth_bridge = EthBridge()

tx = eth_bridge.contract.functions.order_migration(
    Web3.toChecksumAddress("0x5036bf1c86b03dc74bcf490ea5fbad4426069069"),
    40,
    bytes.fromhex("0x747a3157487970615735684268625355744b7175746b44745465354a6944434c53704446".removeprefix('0x'))
).buildTransaction({
    'nonce': Eth(eth_bridge.w3).getTransactionCount(eth_signer.public_key),
    "from": eth_signer.public_key,
}) 

print(
    Eth(eth_bridge.w3).getTransactionCount(eth_signer.public_key)
)

print(tx)
signed_tx = eth_signer.sign_transaction(tx)
resp = eth_bridge.w3.eth.send_raw_transaction(signed_tx.rawTransaction) 
print(resp.hex())