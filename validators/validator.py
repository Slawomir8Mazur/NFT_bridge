import requests
import json
from flask import Flask, request
from utils.signer_eth import EthSigner
from utils.signer_tezos import TezSigner
from utils.contract_wrapper import EthBridge, EthNft
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

class Validator:
    def __init__(self):
        self.config = {
            "ETH_BRIDGE_ADDRESS": "0x72811b6b77d121dccf672dac95fae2f83ab32552",
            "TEZ_BRIDGE_ADDRESS": "KT1TZrzSn39VdRrQvio8j7JZk6mbCta4bRue",

            "ETH_NFT_ADDRESS": "0xafbebd2c8d0ce1022cb8fec1dd744e9f8a54299a",
            "TEZ_NFT_ADDRESS": "KT1QawzpJ7ibUQAjCs98KXSTUrg2K4tEgFf3",
        }
        self.trusted_signers = {
            "0x66665824128f77Cc2b722A5768914131312e4dC4": "http://172.1.0.2:80",
            "0x4b3899157921035c76dac469101663ff34Dbc992": "http://172.1.0.3:80",
            "0xdba01494fe398c5387fA1EDa3D6098364C99F7c5": "http://172.1.0.4:80",
            "0x0DE1F8Aa263E642ec8932FE15076f829295fA464": "http://172.1.0.5:80",
            "0xD0a7efE60Fd0850FDc2A63795a4a55460e732f1c": "http://172.1.0.6:80"
        }

        self.eth_bridge = EthBridge(self.config["ETH_BRIDGE_ADDRESS"])
        self.eth_signer = EthSigner()
        self.tez_signer = TezSigner()
        self.eth_nft = EthNft(self.config["ETH_NFT_ADDRESS"])

        self._cache = {}

    def handler_order_unmmint(self):
        orders = self.tez_signer.get_unmint_metadata(unmint_bigmap_id=133518, token_metadata_bigmap_id=133522)
        for message in orders:
            # Forge message
            self.forge_eth_unmint_message(message)
            self.forge_tez_unmint_message(message)

            # Sign messages
            self.sign_message_eth(message)
            self.sign_message_tez(message)

            # Broadcast message to nodes for signing
            self.broadcast(message)

            # Send to blockchain
            self.send_unmigrate_token_to_ethereum(message)
            self.send_unmint_token_to_tezos(message)
    


    def handler_order_mint(self):
        orders = self.eth_bridge.get_order_metadata()
        for message in orders:
            # Finish forging transaction metadata
            self.forge_tez_mint_transaction_metadata(message, target_account=message["metadata_eth"]["target_address"])
            
            # Get token metadata
            self.forge_tez_mint_token_metadata(message)

            # Forge messages
            self.forge_eth_mint_message(message)
            self.forge_tez_mint_message(message)

            # Cache message
            # if self._cache.get(message["message_eth"]):
            #     continue
            # else:
            #     self._cache[message["message_eth"]] = message

            # Sign messages
            self.sign_message_eth(message)
            self.sign_message_tez(message)

            # Broadcast message to nodes for signing
            self.broadcast(message)

            # Send to blockchain
            self.send_mint_token_to_tezos(message)
            self.send_execute_order_to_ethereum(message)


    #################### METADATA TOOLS ############################
    def forge_tez_mint_transaction_metadata(self, message, target_account):
        message["metadata_tez"] = {
            "exp_block": self.tez_signer.get_level()+10,
            "target_account": target_account,
            "target_amount": 1, 
            "token_id": self.tez_signer.get_storage_value("all_tokens", self.config["TEZ_NFT_ADDRESS"]),
        }
    
    def forge_tez_mint_token_metadata(self, message) -> str:
        message["metadata_tez"]["token_metadata"]= {
            "": "0x"+bytes(self.eth_nft.get_token_uri(message["metadata_eth"]["token_id"]), "utf-8").hex(),
            "decimals": "0x"+bytes("0", "utf-8").hex(),
            "name": "0x"+bytes(self.eth_nft.get_name(), "utf-8").hex(),
            "original_contract": "0x"+bytes(message["metadata_eth"]["token_address"], "utf-8").hex(),
            "original_token_id": "0x"+bytes(str(message["metadata_eth"]["token_id"]), "utf-8").hex(),
            "symbol": "0x"+bytes(self.eth_nft.get_symbol(), "utf-8").hex(),
        }
        message["metadata_tez"]["parsed_token_metadata"] = "{ " + " ; ".join( [f'Elt "{k}" {v}' for k,v in message["metadata_tez"]["token_metadata"].items()] ) + " }"

    #################### MESSAGE TOOLS ############################
    def forge_eth_mint_message(self, message):
        message["message_eth"] = self.eth_bridge.get_order_sign_hash(
            requester_address=message["metadata_eth"]["requester_address"], 
            nft_contract_address=message["metadata_eth"]["token_address"], 
            token_id=message["metadata_eth"]["token_id"]
        )   
    
    def forge_tez_mint_message(self, message):
        token_metadata = message["metadata_tez"]["parsed_token_metadata"]
        message["message_tez"] = self.tez_signer.hash_data(
            data=f"""Pair (Pair (Pair "{message["metadata_tez"]["target_account"]}" {message["metadata_tez"]["target_amount"]}) (Pair {token_metadata} {message["metadata_tez"]["token_id"]})) {message["metadata_tez"]["exp_block"]}""", 
            datatype="pair (pair (pair address nat) (pair (map string bytes) nat)) nat"
        )   

    def forge_eth_unmint_message(self, message):
        message["message_eth"] = self.eth_bridge.get_unmigrate_sign_hash(
            target_owner=message["metadata_tez"]["target_owner_address"], 
            nft_contract_address=message["metadata_tez"]["target_token_address"],
            token_id=message["metadata_tez"]["target_token_id"]
        )   
    
    def forge_tez_unmint_message(self, message):
        message["message_tez"] = self.tez_signer.hash_data(
            data=f"""Pair (Pair "{message["metadata_tez"]["source_address"]}" (Pair {message["metadata_tez"]["amount"]} {message["metadata_tez"]["source_token_id"]})) {message["metadata_tez"]["exp_block"]}""", 
            datatype="pair (pair address (pair nat nat)) nat",
        )  

    ###################### SIGN MESSAGE ############################
    def sign_message_eth(self, message):
        self._cache.setdefault(message["message_eth"], self.eth_signer.sign_hash(message["message_eth"]))

        message.setdefault("signatures_eth", {})
        message["signatures_eth"][self.eth_signer.public_key] = self._cache[message["message_eth"]]

    def sign_message_tez(self, message):
        self._cache.setdefault(message["message_tez"], self.tez_signer.sign_hash_data(message["message_tez"]))

        message.setdefault("signatures_tez", {})
        message["signatures_tez"][self.tez_signer.public_key] = self._cache[message["message_tez"]]


    ###################### NETWORKING TOOLS ############################
    def broadcast(self, message):
        for uri in self.trusted_signers.values():
            if not uri:
                continue
            try:
                msg_signed = json.loads(requests.get(f"{uri}/sign", json=message).text)
                message["signatures_eth"] |= msg_signed["signatures_eth"]
                message["signatures_tez"] |= msg_signed["signatures_tez"]
            except Exception as e:
                print(str(e))
    
    def send_mint_token_to_tezos(self, message):
        token_metadata = message["metadata_tez"]["parsed_token_metadata"]
        concat_sigs = "{ " + " ; ".join( ['"'+i+'"' for i in message['signatures_tez'].values()] ) + " }"

        call_results = self.tez_signer.call_endpoint(
            entrypoint="mint_token", 
            argument=f'Pair {message["metadata_tez"]["exp_block"]} (Pair (Pair (Pair "{message["metadata_tez"]["target_account"]}" {message["metadata_tez"]["target_amount"]}) (Pair {token_metadata} {message["metadata_tez"]["token_id"]})) {concat_sigs} )', 
            extra_fields=["--burn-cap", "0.2"])
        resp = " ".join(i.decode('utf-8') for i in call_results)
        if "FAILED" in resp:
            raise Exception(f"Tezos mint failed with following message:\n{resp}")
        return resp

    def send_execute_order_to_ethereum(self, message):
        sign_concat = self.eth_signer.concat_signatures(
            [s for s in message["signatures_eth"].values()]
        )
        resp = self.eth_bridge.call_execute_migration(
            message["metadata_eth"]["requester_address"],
            message["metadata_eth"]["token_address"],
            message["metadata_eth"]["token_id"],
            sign_concat,
            self.eth_signer            
        )
        with open("log_send_eth.txt", "w") as f:
            f.write(str(resp))
            print(str(resp))

    def send_unmigrate_token_to_ethereum(self, message):
        sign_concat = self.eth_signer.concat_signatures(
            [s for s in message["signatures_eth"].values()]
        )
        self.eth_bridge.call_unmigrate_token(
            target_owner=message["metadata_tez"]["target_owner_address"],
            nft_contract_address=message["metadata_tez"]["target_token_address"],
            token_id=message["metadata_tez"]["target_token_id"],
            signatures=sign_concat,
            eth_signer=self.eth_signer            
        )
    
    def send_unmint_token_to_tezos(self, message):
        concat_sigs = "{ " + " ; ".join( ['"'+i+'"' for i in message['signatures_tez'].values()] ) + " }"

        call_results = self.tez_signer.call_endpoint(
            entrypoint="unmint_token", 
            argument=f'Pair {message["metadata_tez"]["exp_block"]} (Pair {concat_sigs} (Pair "{message["metadata_tez"]["source_address"]}" (Pair {message["metadata_tez"]["amount"]} {message["metadata_tez"]["source_token_id"]})))',
            extra_fields=["--burn-cap", "0.02"])
        resp = " ".join(i.decode('utf-8') for i in call_results)
        if "FAILED" in resp:
            raise Exception(f"Tezos mint failed with following message:\n{resp}")
        return resp


validator = Validator()

@app.route('/sign')
def sign():
    # assert request.remote_addr in trusted_signers.values(), "sender's IP is untrusted"
    message = request.json

    # Cache message
    # validator._cache.setdefault(message["message_eth"], message)

    # Sign message
    validator.sign_message_eth(message)
    validator.sign_message_tez(message)
    return json.dumps(message)

# @app.route('/trust')
# def trust():
#     """
#     works for curl.exe -X POST "localhost:8000/trust?message=a04f8cb4209134f3655c38b889d4bd4f98ba20cb3c4c7f85f74dc16c805633c4&eth_signature=62350e01d69830e361abcf2bef93543195b7f7b2058adf4fda4ebacef9bd3c585cb759e0798cf7923d7041e9e147f5dfed5433a68a3d40eecc747c287749b4b61c"
#     """
#     caller_ip = f"http://{request.remote_addr}:80"
#     message = request.args.get('message')
#     eth_signature = request.args.get('eth_signature')
#     signer = EthSigner.get_signer(message, eth_signature, validate=False)

#     if signer in validator.trusted_signers:
#         if caller_ip in validator.trusted_signers.values():
#             return f"IP {caller_ip} was already entrusted before"
#         else:
#             validator.trusted_signers[signer] = caller_ip
#             return f"IP {caller_ip} has been entrusted"
#     return f"IP {request.remote_addr} was NOT entrusted, {signer} is not entrusted address"

# @app.route('/get/trusted', methods=['GET'])
# def get_trusted():
#     return json.dumps(validator.trusted_signers)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=validator.handler_order_unmmint, 
        trigger="interval", 
        seconds=30,
        max_instances=4
    )
    scheduler.start()
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=validator.handler_order_mint, 
        trigger="interval", 
        seconds=10,
        max_instances=4
    )
    scheduler.start()
    
    app.run(host="0.0.0.0", port=80)