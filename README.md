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

## Ethereum part

* Build with
```bash
vyper -f bytecodeabi eth_components\main.py
```
* Deploy at https://www.myetherwallet.com/wallet/deploy
* Test: manually for now at https://www.myetherwallet.com/wallet/interact

## Tezos part

 TODO

## Validators

I will provide docker images for running validators

TODO

## Sources

* https://github.com/vyperlang/vyper/blob/master/examples/wallet/wallet.vy
* https://reference.auditless.com/cheatsheet/