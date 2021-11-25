# NFT bridge

## Description

Project is meant to have following items:

1. Tezos smart-contract that:
    * accepts FA2 tokens as a collateral for their match minted on Ethereum network
    * gives back collateral FA2 token if user on requested it on Ethereum bockchain
    * is a factory for FA2 contracts for tokens that should be minted on Tezos blockchain, having ERC721 as collateral - those FA2 contracts should mirror their ethereum's counterparts
    * validates some actions with multisig
2. Ethereum smart-contract that mirror it's Tezos counterpart
3. Network of validators - initially there will be 5 validators, from which 3 would need to agree on minting token on the other chain or burning them

### Future view

Proposed implementation assumes there are validators - programs that comunicates with each other where majority of them can confirm taking action. Current implementation requires that majority of them is honest, for transactions on both chains there, validators crate pair of signatures to authorize their actions.

In future implementation I'd like to update approach to signatures, so that every process is signed only once. In that case when validators would confirm with their signature deposit on one chain, user could take that signature and claim token on the other chain. That concept requires some fine-graining, but would give even smaller edge for any mischief.


# Run

### Backend

Requirements:

`Docker`

**Run**

In file docker-compose.yml replace all *PUT_SECRET_HERE* with infura ethereum project id (more info in [infura documentation](https://infura.io/docs/ethereum#section/Securing-Your-Credentials) and at [infura website](https://infura.io/dashboard/ethereum))

```bash
docker build -t validators .
docker-compose up
```

### Frontend

Requirements:

`Node v16.13.0`

`Yarn v1.22.15`

**Run**

```bash
cd website
yarn install
yarn start
```

## Build contracts

### Ethereum part

Requirements:
* python 3.9
* `vyper` python package

* Build with
```bash
vyper -f bytecode .\eth_components\contracts\main.vy > .\eth_components\builds\bytecode.txt
vyper -f abi .\eth_components\contracts\main.vy > .\eth_components\builds\abi.txt
```
* Deploy at https://www.myetherwallet.com/wallet/deploy
* Test: manually for now at https://www.myetherwallet.com/wallet/interact
* Automated tested with tools from `validator/utils/contract_wrapper.py` and `validator/utils/signer_eth.py`

### Tezos part

* Build by copy-pasting the code at https://smartpy.io/ide 
* Deploy through smartpy.io UI or tezos-client

### Components status

1. Eth contract
* Is done, user can order minting
* If validators won't pick up an order within an hour user can also cancel order and get back token
2. Validators
* validators containers cluster nicely with predefined ip, as it is done currently
* single minting and unminting process works properly
* there can be user orders that validators wouldn't be able to fullfill nor remove, in that case validators for now would try to fullfill it periodically, each several seconds
* In next iterations of this project there should be implemented some mechanizm to remove invalid orders or prevent orders from being/becoming invalid - it would be nice optimisation
3. Tezos contract
* Current version works for our usecase
* Requires some refactoring for: better handling order validation, user withdrawing request of order (helps if validators are idle), more tests, increasing readability for review
I'm finishing development, multisig works, minting and burning are in test phase 
4. UI
* Works, current version is very basic and allows only token migration and unmigration
* In future interface could provide actions for situations when validators are idle and visual representation of existing tokens

# Examples

#### Migrating ERC721 token to Tezos

1. Call `Approve` endpoint in ERC721 contract with parameters `_address`- address of bridge developed here, latest is `0xFE37dd9D3528737f55D1bd8137F4ca67CDcf61fA`, `_tokenId`-id of token you want to migrate, it should be int value
2. Call `Order_migration` at `0xFE37dd9D3528737f55D1bd8137F4ca67CDcf61fA` with `nft_contract`- address of you contract, I use `0x5036bf1c86b03dc74bcf490ea5fbad4426069069`, `token_id`-id of your token, `target_account`- hex of tezos account, can be `0xa04f8cb4209134f3655c38b889d4bd4f98ba20cb3c4c7f85f74dc16c805633c4`
3. The token will pop up in your tezos wallet now

## Sources

* https://github.com/vyperlang/vyper/blob/master/examples/wallet/wallet.vy
* https://reference.auditless.com/cheatsheet/