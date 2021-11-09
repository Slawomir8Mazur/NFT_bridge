import os
import requests
import json
from flask import Flask, request
from utils.signer_eth import EthSigner
from utils.signer_tezos import TezSigner
from utils.contract_wrapper import EthBridge
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

eth_bridge = EthBridge()
eth_signer = EthSigner()
tez_signer = TezSigner()

cache = {}

trusted_signers = {
    "0x66665824128f77Cc2b722A5768914131312e4dC4": "http://172.1.0.2:80",
    "0x4b3899157921035c76dac469101663ff34Dbc992": "http://172.1.0.3:80",
    "0xdba01494fe398c5387fA1EDa3D6098364C99F7c5": "http://172.1.0.4:80",
    "0x0DE1F8Aa263E642ec8932FE15076f829295fA464": "http://172.1.0.5:80"
    "0xD0a7efE60Fd0850FDc2A63795a4a55460e732f1c": "http://172.1.0.6:80",
}

def sign_message(message, eth_signer=eth_signer, tez_signer=tez_signer):
    return {
        eth_signer.public_key: {
            "signature_eth": eth_signer.sign_hash(message),
            "signature_tez": tez_signer.sign_hash(message),
            "address_tez": tez_signer.public_key
        }    
    }

def broadcast(message):
    for uri in trusted_signers.values():
        if uri:
            try:
                msg_signed = json.loads(requests.get(f"{uri}/sign", json=message).text)
                message["signatures"] |= msg_signed.get("signatures", {})
            except Exception as e:
                with open("logs3.txt", "w") as f:
                    f.write(str(e))
    return message

def send_to_eth(message):
    sign_concat = eth_signer.concat_signatures(
        [sign["signature_eth"] for sign in message["signatures"].values()]
    )
    try:
        eth_bridge.call_execute_migration(
            message["metadata"]["requester_address"],
            message["metadata"]["token_address"],
            message["metadata"]["token_id"],
            sign_concat,
            eth_signer            
        )
    except Exception as e:
        print(str(e))

def sign_broadcast_send(message):
    message["message"] = eth_bridge.get_order_sign_hash(
        requester_address=message["metadata"]["requester_address"], 
        nft_contract_address=message["metadata"]["token_address"], 
        token_id=message["metadata"]["token_id"]
    )
    message["signatures"] = sign_message(
        bytes.fromhex(message["message"].removeprefix("0x"))
    )
    cache[message["message"]] = message
    broadcast(message)
    send_to_eth(message)

@app.route('/sign')
def sign():
    # assert request.remote_addr in trusted_signers.values(), "sender's IP is untrusted"
    message = request.json
    message["signatures"] |= sign_message(
        bytes.fromhex(message["message"].removeprefix("0x"))
    )
    return json.dumps(message)

@app.route('/trust')
def trust():
    """
    works for curl.exe -X POST "localhost:8000/trust?message=a04f8cb4209134f3655c38b889d4bd4f98ba20cb3c4c7f85f74dc16c805633c4&eth_signature=62350e01d69830e361abcf2bef93543195b7f7b2058adf4fda4ebacef9bd3c585cb759e0798cf7923d7041e9e147f5dfed5433a68a3d40eecc747c287749b4b61c"
    """
    caller_ip = f"http://{request.remote_addr}:80"
    message = request.args.get('message')
    eth_signature = request.args.get('eth_signature')
    signer = EthSigner.get_signer(message, eth_signature, validate=False)

    if signer in trusted_signers:
        if caller_ip in trusted_signers.values():
            return f"IP {caller_ip} was already entrusted before"
        else:
            trusted_signers[signer] = caller_ip
            return f"IP {caller_ip} has been entrusted"
    return f"IP {request.remote_addr} was NOT entrusted, {signer} is not entrusted address"

@app.route('/get/trusted', methods=['GET'])
def get_trusted():
    return json.dumps(trusted_signers)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=(lambda: eth_bridge.get_order_metadata(sign_broadcast_send)), 
        trigger="interval", 
        seconds=10,
        max_instances=4
    )
    scheduler.start()
    
    app.run(host="0.0.0.0", port=80)