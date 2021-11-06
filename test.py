from flask import Flask, request

app = Flask(__name__)

@app.route('/trust', methods=['GET', 'POST'])
def trust():
    """
    works for curl.exe -X POST "localhost:8000/trust?message=a04f8cb4209134f3655c38b889d4bd4f98ba20cb3c4c7f85f74dc16c805633c4&eth_signature=62350e01d69830e361abcf2bef93543195b7f7b2058adf4fda4ebacef9bd3c585cb759e0798cf7923d7041e9e147f5dfed5433a68a3d40eecc747c287749b4b61c"
    """
    message = request.args.get('message')
    eth_signature = request.args.get('eth_signature')
    return f"IP {request.remote_addr}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)