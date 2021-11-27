import json
import os
import requests
import subprocess
    
class TezSigner:
    bridge_address="KT1TZrzSn39VdRrQvio8j7JZk6mbCta4bRue"
    _account_name = "acc"
    _endpoint = 'https://granadanet.smartpy.io'
    # _endpoint = 'https://rpc.tzkt.io/granadanet'
    
    def __init__(self):
        self.validate()
        self.update_endpoint()
        self.public_key = self._register_account()

    @classmethod
    def _call_cmd(cls, cmd:str):
        return cls._call_cmd_square(cmd.split())

    @staticmethod
    def _call_cmd_square(cmd:str, test=True):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        resp = process.communicate()[0]
        if test:
            assert resp, f"Empty response for {cmd}, make sure everything worked"
        return resp.split()

    @staticmethod
    def validate():
        if not os.environ.get("TEZOS_PRIVATE_KEY"):
            raise EnvironmentError("Set TEZOS_PRIVATE_KEY environment variable")

    @classmethod
    def update_endpoint(cls):
        return cls._call_cmd_square(["tezos-client", "-E", cls._endpoint, "config", "update"], test=False)

    @classmethod
    def _register_account(cls):
        return str(cls._call_cmd(f"tezos-client import secret key {cls._account_name} unencrypted:{os.environ['TEZOS_PRIVATE_KEY']}")[-1], 'utf-8')
    
    @classmethod
    def _cleanup(cls):
        return cls._call_cmd(f"tezos-client forget address {cls._account_name} --force")

    @classmethod
    def get_edpk(cls):
        return cls._call_cmd(f"tezos-client show address {cls._account_name}")[-1].decode('utf-8')

    @classmethod
    def get_tz1(cls):
        return cls._call_cmd(f"tezos-client show address {cls._account_name}")[1].decode('utf-8')

    @classmethod
    def hash_data(cls, data, datatype):
        """returns packed data"""
        cmd = ['tezos-client', 'hash', 'data', data, 'of', 'type', datatype]
        return cls._call_cmd_square(cmd)[3].decode('utf-8')

    @classmethod
    def sign_hash_data(cls, hash_hex: str):
        """returns blake2b"""
        return cls._call_cmd(f"tezos-client sign bytes {hash_hex} for {cls._account_name}")[-1].decode('utf-8')

###################### CONTRACT CALLS ####################################
    @classmethod
    def call_endpoint(cls, entrypoint, argument, extra_fields):
        """
        >>> tez_signer.call_endpoint("mint_token", 'Pair (Pair (Pair "tz1iXPT2VmUJAy27KfwAyK2XnjoEtQfbn3SB" 1) (Pair {} 0)) (Pair (Pair 0x7dea9dd8b6caa0f3de0e6aa79ac9e09a328a5c9907be5dbdacd1139fbb073a8c9ceb3187145d522b736015dbf3ef8f5c4f08f8d431279b0980e2852be683ccec { "edsigu4g8bjbfNKrzYbLSPAzCrvqwa2qqPs2BcHeEJkaXHZmygD1pwE9X7JpcT2nvmJhxS4TvcH1TJ3VGPtLLdYbyyYLmyq69G8" ; "edsigtgUF6zdkawH2KooTgR6ZrTNWKR24BwE6xhLBsqqv5L4NmUmFS7daQXoNAWcGcfK423wxiBLWPu4xNekBTgqSaUC1EU2WjZ" ; "edsigtbfjtsNHc5FPJgWSBoLmNhTQKv4s1Ea7DfjJ8nHvqJmujTjW414wpwe4bAPM5bGdj4YbAtACFZiGzuYFaJcmS8i1MdzDJ5" }) "")')
        """
        return cls._call_cmd_square([
            "tezos-client", "-w", "2", "transfer", "0", 
            "from", cls._account_name, 
            "to", cls.bridge_address, 
            "--entrypoint", entrypoint,
            "--arg", argument, *extra_fields])
    
    @classmethod
    def originate(cls, storage, contract_path, extra_fields, name="new_contract"):
        return cls._call_cmd_square([
            "tezos-client", "originate", 
            "contract", name, 
            "transferring", "0", 
            "from", cls._account_name, 
            "running", contract_path, 
            "--init", storage,
            *extra_fields
        ])[-1].decode('utf-8')
    
######################## API TOOLS #######################################
    @staticmethod
    def get_storage_value(field_name, contract_address, network="granadanet"):
            resp = requests.get(f"https://api.better-call.dev/v1/contract/{network}/{contract_address}/storage")
            resp_json = json.loads(resp.text)
            return [record['value'] for record in resp_json[0]['children'] if record.get('name')==field_name][0]

    @staticmethod
    def _get_bigmap(bigmap_id: int, network="granadanet"):
        raise DeprecationWarning

    @staticmethod
    def _get_bigmap_new(key, bigmap_id: int, network="granadanet"):
        if network=="granadanet":
            resp = requests.get(f"https://api.granadanet.tzkt.io/v1/bigmaps/{bigmap_id}/keys/{key}")
        elif not network or network=="mainnet":
            resp = requests.get(f"https://api.tzkt.io/v1/bigmaps/{bigmap_id}/keys/{key}")
        else:
            raise NotImplementedError
        return json.loads(resp.text)
    
    @staticmethod
    def get_level(network="granadanet") -> int:
            resp = requests.get(f"https://api.better-call.dev/v1/head")
            resp_json = json.loads(resp.text)
            return [record['level'] for record in resp_json if record['network']==network][0]

    @classmethod
    def get_unmint_metadata(cls, unmint_bigmap_id: int, token_metadata_bigmap_id: int, network="granadanet"):
        resp = cls._get_bigmap_new("", unmint_bigmap_id, network)
        messages = [{"metadata_tez": {
            "source_address": record['key']['address'],
            "source_token_id": record['key']['token_id'],
            "amount": record['key']['amount'],
            "target_owner_address": record['value'],
            "exp_block": cls.get_level()+10,}} 
            for record in resp
            if record["active"]
        ]
        for message in messages:
            resp = cls._get_bigmap_new(
                key=message["metadata_tez"]["source_token_id"],
                bigmap_id=token_metadata_bigmap_id
            )
            message["metadata_tez"]["target_token_id"] = int(bytes.fromhex(resp['value']['token_info']['original_token_id']).decode('utf-8'))
            message["metadata_tez"]["target_token_address"] = bytes.fromhex(resp['value']['token_info']['original_contract']).decode('utf-8')
        return messages

def test():
    try:
        TezSigner._cleanup()
    except:
        pass
    tez_signer = TezSigner()
    hashed_data = tez_signer.hash_data('"tz1fAtHNz8cz5f4QqZtCaGRrnJteVNpRzL3y"', "address")
    sig = tez_signer.sign_hash_data(hashed_data)
    # print(sig)

    hashed_data = tez_signer.hash_data('Pair "tz1fAtHNz8cz5f4QqZtCaGRrnJteVNpRzL3y" (Pair 1 0)', "pair address (pair nat nat)")
    print(f"{tez_signer.get_edpk()=}")
    print(f"{hashed_data=}")
    print(f"{tez_signer.sign_hash_data(hashed_data)=}")
# test()

def deploy_bridge():
    """https://granadanet.tzkt.io/opJaKxDUWF7BK8impcMqMvv3QVp7UkbkdbweADbtoJjFVYTJf3S"""
    tez_signer = TezSigner()
    bridge_address = tez_signer.originate(
        storage='(Pair (Pair "tz1SW56fUwARi14KJcn6bNtErFK8ocE2yq3m" {"edpktfiDrD2tgdbFbZkoCSFmZdfsS4BUnETtGQJonYsL5MXPV7KrTK"; "edpkvavyHRRWsG7oFiMw6GHDWXMrHZg5U9bvfgeorRGxcpfeaZh9Ev"; "edpku5DskWhVQqi5FJYjMqpHHrgWQhoqVqFm3GL5hqkz29ubkcP8BJ"; "edpkv3J5HfkH9BDbG83KdGvhWNpgVSzfoUqLuKpRuWZYvqHXyVXH6D"; "edpkuW9FxUfSe2dUijYZzoQUmY8XfYpeBrJ1HDW3zXVhrLw4ycXT55"}) (Pair {} 3))', 
        contract_path="tezos_components/compiled/bridge_contract", name="tez_bridge", extra_fields=["--burn-cap", "0.6"])
    print(bridge_address)

def deploy_nft():
    """https://granadanet.tzkt.io/KT1TZrzSn39VdRrQvio8j7JZk6mbCta4bRue"""
    tez_signer = TezSigner()
    nft_address = tez_signer.originate(
        storage='(Pair (Pair "tz1fAtHNz8cz5f4QqZtCaGRrnJteVNpRzL3y" (Pair 0 {})) (Pair (Pair {Elt "" 0x697066733a2f2f516d52537653587534426648317143757743746751657167457a7a6b6f5173373369745458584a6935667938584e} {}) (Pair False {})))', 
        contract_path="tezos_components/compiled/nft_unsafe", name="nft", extra_fields=["--burn-cap", "1.14"])
    print(nft_address)

def set_minter_get_signature():
    """https://granadanet.tzkt.io/KT1QawzpJ7ibUQAjCs98KXSTUrg2K4tEgFf3"""
    tez_signer = TezSigner()
    level = TezSigner.get_level()+1000
    print(f"{level=}")
    hashed_data = tez_signer.hash_data(f'Pair "KT1QawzpJ7ibUQAjCs98KXSTUrg2K4tEgFf3" {level}', "pair address nat")
    print(f"{hashed_data=}")
    print(f"{tez_signer.sign_hash_data(hashed_data)=}")

def set_minter():
    tez_signer = TezSigner()
    call_results = tez_signer.call_endpoint(
        entrypoint="set_minter", 
        argument='Pair 683063 (Pair "KT1QawzpJ7ibUQAjCs98KXSTUrg2K4tEgFf3" { "edsigtaDcSRyyNy5UG5dzRQ5DZd3qZx9ebqMAzbtFfJV9Kox6zLagNkmAj9tqTRhEHtj6c6MN88vSKnx3CvSVsxFo6xwWEsAnb1" ; "edsigtb2T52nHSFsLWpZhzxQLrKKTYeRXWA6HNWvBRbxg6wyo2MSNXDV7YoSx1KFcT8afVdRzjukkmLLrzxoUyxeiFFhSuSLAjA" ; "edsigtaSrrtXG4KogJgiFuP2F6i3cKhtZvUW49HHbqaQso1zVtmSDRGZ6jwXNFGiFaTUqGb8ATPxTnoLqxCtcBUYq15Qkhfd9zr" ; "edsigteLi468ydKy93msK3L6VZ8YGZQufNjXJDF2nGAvcmG2rent6NhZeFL3FchHMPW79kyHotkzPp2GFVyfxSuA6HXnFpYFKr9" ; "edsigtq988bxRFH5XtoPuM9RTwKwAHpXP2bzAwQC44G1WTLq2F9uLSsyDMtTUbxUkzKjZ6JYNQ4VbKbDbVPwUdeJgdKNg4TFar5" })', 
        extra_fields=["--burn-cap", "1.14"])
    print(call_results)
