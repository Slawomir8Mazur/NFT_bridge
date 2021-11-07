# NFT bridge

## Description

Project is meant to have following items:

1. Tezos smart-contract that:
    * accepts FA2 tokens as a collateral for their match minted on Ethereum network
    * gives back collateral FA2 token if user on requested it on Ethereum bockchain
    * is a factory for FA2 contracts for tokens that should be minted on Tezos blockchain, having ERC721 as collateral - those FA2 contracts should mirror their ethereum's counterparts
    * validates some actions with multisig
2. Ethereum smart-contract that mirror it's Tezos counterpart
3. Network of validators - initially there will be 5 validators, from which 3 whould need to agree on mining token on the other chain or burning them

### Future view

Proposed implementation assumes there are validators - programs that comunicates with each other where majority of them can confirm taking action. Current implementation requires that majority of them is honest, for transactions on both chains there, validators crate pair of signatures to authorize their actions.

In future implementation I'd like to update approach to signatures, so that every process is signed only once. In that case when validators would confirm with their signature deposit on one chain, user could take that signature and claim token on the other chain. That concept requires some fine-graining, but would give even smaller edge for any mischief. 

### Ethereum part

* Build with
```bash
vyper -f bytecode .\eth_components\contracts\main.vy > .\eth_components\bytecode.txt
vyper -f abi .\eth_components\contracts\main.vy > .\eth_components\abi.txt
```
* Deploy at https://www.myetherwallet.com/wallet/deploy
* Test: manually for now at https://www.myetherwallet.com/wallet/interact
* Automated tested with tools from `validator/utils/contract_wrapper.py` and `validator/utils/signer_eth.py`

### Tezos part

* Build by copy-pasting the code at https://smartpy.io/ide 


Current development phase:
1. Multisig functionality works
2. 

### Validators

Build and run with
```bash
docker build -t validators . && docker run -p 8000:80 -e "INFURA_URI=https://ropsten.infura.io/v3/PROJECT_SECRET_KEY" -e ETHEREUM_PRIVATE_KEY=78d003... -e TEZOS_PRIVATE_KEY=edsk3n... validators:latest
```

## Development phase

### General overview

For now it will be one side bridge - allows to migrate ERC721 to Tezos and back again. I will not work yet the other way - FA2 tokens will not be minted on Ethereum blockchain.

### Components status

1. Eth contract
* Is done, user can order minting
* If validators won't pick up an order within an hour user can also cancel order and get back token
2. Validators
* validators containers works properly as separate instances, but they have troubles with clustering, so it's problem to gather enough signatures to confirm transaction
* with tools develop for validators one can run all validators in localy, but I target to focus on development here and make it work properly in decentralized envirnoment   
3. Tezos contract
* I'm finishing development, multisig works, minting and burning are in test phase 
4. UI
* not started, I'm focusing on working backend
* users can still work through it through CLI tools or MyEtherWallet

## Sources

* https://github.com/vyperlang/vyper/blob/master/examples/wallet/wallet.vy
* https://reference.auditless.com/cheatsheet/