from flask import Flask, request
from utils.signer_eth import EthSigner
from utils.signer_tezos import TezSigner

app = Flask(__name__)

eth_signer = EthSigner()
tez_signer = TezSigner()

trusted_eth_signers = [
    "0xD0a7efE60Fd0850FDc2A63795a4a55460e732f1c",
    "0x66665824128f77Cc2b722A5768914131312e4dC4",
    "0x4b3899157921035c76dac469101663ff34Dbc992",
    "0xdba01494fe398c5387fA1EDa3D6098364C99F7c5",
    "0x0DE1F8Aa263E642ec8932FE15076f829295fA464"
]

trusted_addresses = []


@app.route('/trust', methods=['GET', 'POST'])
def trust():
    """
    works for curl.exe -X POST "localhost:8000/trust?message=a04f8cb4209134f3655c38b889d4bd4f98ba20cb3c4c7f85f74dc16c805633c4&eth_signature=62350e01d69830e361abcf2bef93543195b7f7b2058adf4fda4ebacef9bd3c585cb759e0798cf7923d7041e9e147f5dfed5433a68a3d40eecc747c287749b4b61c"
    """
    message = request.args.get('message')
    eth_signature = request.args.get('eth_signature')
    if (signer:=EthSigner.get_signer(message, eth_signature, validate=False)) in trusted_eth_signers:
        trusted_addresses.append(request.remote_addr)
        return f"IP {request.remote_addr} is entrusted"
    return f"IP {request.remote_addr} was NOT entrusted, {signer} is not trusted"

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    """
    Works for:
    curl.exe -X GET localhost:8000/sign?message=a04f8cb4209134f3655c38b889d4bd4f98ba20cb3c4c7f85f74dc16c805633c4
    """
    assert request.remote_addr in trusted_addresses, "sender's IP is untrusted"
    message_str = request.args.get('message')
    assert message_str, AssertionError("no message provided as a parameter")
    message = bytes.fromhex(message_str.removeprefix("0x"))
    return {
        "message": message.hex(),
        "signatures": [
            {
                "type": "ethereum",
                "address": eth_signer.public_key,
                "signature": eth_signer.sign_hash(message)
            },
            {
                "type": "tezos",
                "address": tez_signer.public_key,
                "signature": tez_signer.sign_hash(message)
            }
        ]
    }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)