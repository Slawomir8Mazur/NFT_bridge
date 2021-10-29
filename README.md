# NFT_bridge

## Deploy Eth part

Build with
```
vyper -f abi eth_components\main.py
```
Deploy at https://www.myetherwallet.com/wallet/deploy
<!-- docker run -v D:\coding\NFT_bridge:/code vyperlang/vyper /code/<contract_file.vy> -->

### Helpers
Run interactive vyper container
```
docker run -it --entrypoint /bin/bash vyperlang/vyper
```

## Build Tezos part