import sys
sys.path.append("/app/validators")

from utils.contract_wrapper import EthNft, EthBridge
from utils.signer_eth import EthSigner
from random import randint
from time import sleep

config = {
    "ETH_BRIDGE_ADDRESS": "0x72811b6b77d121dccf672dac95fae2f83ab32552",
    "TEZ_BRIDGE_ADDRESS": "KT1TZrzSn39VdRrQvio8j7JZk6mbCta4bRue",
    "ETH_NFT_ADDRESS": "0xafbebd2c8d0ce1022cb8fec1dd744e9f8a54299a",
    "TEZ_NFT_ADDRESS": "KT1QawzpJ7ibUQAjCs98KXSTUrg2K4tEgFf3",
}

eth_bridge = EthBridge(config["ETH_BRIDGE_ADDRESS"])
eth_signer = EthSigner()
eth_nft = EthNft(config["ETH_NFT_ADDRESS"])

token_id = randint(100, 1000)

eth_nft.call_mint(token_id, f"www.test{token_id}.com", eth_signer)
sleep(50)
eth_nft.call_approve(config["ETH_BRIDGE_ADDRESS"], token_id, eth_signer)

print(f"""
{token_id=},
{config["ETH_NFT_ADDRESS"]}
""")