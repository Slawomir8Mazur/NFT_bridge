import React, { useState } from "react";
import { ethers } from "ethers";
import ErrorMessage from "./ErrorMessage";
import TxList from "./TxList";
import { TempleWallet } from '@temple-wallet/dapp';
import { Container, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const startMint = async ({ setErrorMint, setTxsMint, tokenId, tokenUri }) => {
  try {
    if (!window.ethereum)
      throw new Error("No crypto wallet found. Please install it.");
      
    
    await window.ethereum.send("eth_requestAccounts");
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();

    const contractAddress = ethers.utils.getAddress("0xafbebd2c8d0ce1022cb8fec1dd744e9f8a54299a");
    const contractAbi = [{"name": "Transfer", "inputs": [{"name": "sender", "type": "address", "indexed": true}, {"name": "receiver", "type": "address", "indexed": true}, {"name": "tokenId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "Approval", "inputs": [{"name": "owner", "type": "address", "indexed": true}, {"name": "approved", "type": "address", "indexed": true}, {"name": "tokenId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "ApprovalForAll", "inputs": [{"name": "owner", "type": "address", "indexed": true}, {"name": "operator", "type": "address", "indexed": true}, {"name": "approved", "type": "bool", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [], "outputs": []}, {"stateMutability": "view", "type": "function", "name": "supportsInterface", "inputs": [{"name": "_interfaceID", "type": "bytes32"}], "outputs": [{"name": "", "type": "bool"}], "gas": 2641}, {"stateMutability": "view", "type": "function", "name": "balanceOf", "inputs": [{"name": "_owner", "type": "address"}], "outputs": [{"name": "", "type": "uint256"}], "gas": 2925}, {"stateMutability": "view", "type": "function", "name": "ownerOf", "inputs": [{"name": "_tokenId", "type": "uint256"}], "outputs": [{"name": "", "type": "address"}], "gas": 2813}, {"stateMutability": "view", "type": "function", "name": "getApproved", "inputs": [{"name": "_tokenId", "type": "uint256"}], "outputs": [{"name": "", "type": "address"}], "gas": 5040}, {"stateMutability": "view", "type": "function", "name": "isApprovedForAll", "inputs": [{"name": "_owner", "type": "address"}, {"name": "_operator", "type": "address"}], "outputs": [{"name": "", "type": "bool"}], "gas": 3190}, {"stateMutability": "nonpayable", "type": "function", "name": "transferFrom", "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_tokenId", "type": "uint256"}], "outputs": [], "gas": 173314}, {"stateMutability": "nonpayable", "type": "function", "name": "safeTransferFrom", "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_tokenId", "type": "uint256"}], "outputs": [], "gas": 190624}, {"stateMutability": "nonpayable", "type": "function", "name": "safeTransferFrom", "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_tokenId", "type": "uint256"}, {"name": "_data", "type": "bytes"}], "outputs": [], "gas": 190624}, {"stateMutability": "nonpayable", "type": "function", "name": "approve", "inputs": [{"name": "_approved", "type": "address"}, {"name": "_tokenId", "type": "uint256"}], "outputs": [], "gas": 46741}, {"stateMutability": "nonpayable", "type": "function", "name": "setApprovalForAll", "inputs": [{"name": "_operator", "type": "address"}, {"name": "_approved", "type": "bool"}], "outputs": [], "gas": 39516}, {"stateMutability": "nonpayable", "type": "function", "name": "mint", "inputs": [{"name": "_to", "type": "address"}, {"name": "_tokenId", "type": "uint256"}, {"name": "token_uri", "type": "string"}], "outputs": [{"name": "", "type": "bool"}], "gas": 189225}, {"stateMutability": "nonpayable", "type": "function", "name": "burn", "inputs": [{"name": "_tokenId", "type": "uint256"}], "outputs": [], "gas": 119991}, {"stateMutability": "view", "type": "function", "name": "name", "inputs": [], "outputs": [{"name": "", "type": "string"}], "gas": 10946}, {"stateMutability": "view", "type": "function", "name": "symbol", "inputs": [], "outputs": [{"name": "", "type": "string"}], "gas": 10976}, {"stateMutability": "view", "type": "function", "name": "tokenURI", "inputs": [{"name": "_tokenId", "type": "uint256"}], "outputs": [{"name": "", "type": "string"}], "gas": 13413}];
    
    const contract = new ethers.Contract(contractAddress, contractAbi, provider);
    const contractWithSigner = contract.connect(signer)

    const tx = await contractWithSigner.mint(
      window.ethereum.selectedAddress,
      tokenId,
      tokenUri
    );
    
    console.log("tx", tx);
    setTxsMint([tx]);
  } catch (err) {
    setErrorMint(err.message);
  }
};

const orderMigration = async ({ setErrorOrder, setTxsOrder, tokenId, targetAddress }) => {
  try {
    if (!window.ethereum)
      throw new Error("No crypto wallet found. Please install it.");
      
    
    await window.ethereum.send("eth_requestAccounts");
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();

    const nftAddress = ethers.utils.getAddress("0xafbebd2c8d0ce1022cb8fec1dd744e9f8a54299a");
    const nftAbi = [{"name": "Transfer", "inputs": [{"name": "sender", "type": "address", "indexed": true}, {"name": "receiver", "type": "address", "indexed": true}, {"name": "tokenId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "Approval", "inputs": [{"name": "owner", "type": "address", "indexed": true}, {"name": "approved", "type": "address", "indexed": true}, {"name": "tokenId", "type": "uint256", "indexed": true}], "anonymous": false, "type": "event"}, {"name": "ApprovalForAll", "inputs": [{"name": "owner", "type": "address", "indexed": true}, {"name": "operator", "type": "address", "indexed": true}, {"name": "approved", "type": "bool", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [], "outputs": []}, {"stateMutability": "view", "type": "function", "name": "supportsInterface", "inputs": [{"name": "_interfaceID", "type": "bytes32"}], "outputs": [{"name": "", "type": "bool"}], "gas": 2641}, {"stateMutability": "view", "type": "function", "name": "balanceOf", "inputs": [{"name": "_owner", "type": "address"}], "outputs": [{"name": "", "type": "uint256"}], "gas": 2925}, {"stateMutability": "view", "type": "function", "name": "ownerOf", "inputs": [{"name": "_tokenId", "type": "uint256"}], "outputs": [{"name": "", "type": "address"}], "gas": 2813}, {"stateMutability": "view", "type": "function", "name": "getApproved", "inputs": [{"name": "_tokenId", "type": "uint256"}], "outputs": [{"name": "", "type": "address"}], "gas": 5040}, {"stateMutability": "view", "type": "function", "name": "isApprovedForAll", "inputs": [{"name": "_owner", "type": "address"}, {"name": "_operator", "type": "address"}], "outputs": [{"name": "", "type": "bool"}], "gas": 3190}, {"stateMutability": "nonpayable", "type": "function", "name": "transferFrom", "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_tokenId", "type": "uint256"}], "outputs": [], "gas": 173314}, {"stateMutability": "nonpayable", "type": "function", "name": "safeTransferFrom", "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_tokenId", "type": "uint256"}], "outputs": [], "gas": 190624}, {"stateMutability": "nonpayable", "type": "function", "name": "safeTransferFrom", "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_tokenId", "type": "uint256"}, {"name": "_data", "type": "bytes"}], "outputs": [], "gas": 190624}, {"stateMutability": "nonpayable", "type": "function", "name": "approve", "inputs": [{"name": "_approved", "type": "address"}, {"name": "_tokenId", "type": "uint256"}], "outputs": [], "gas": 46741}, {"stateMutability": "nonpayable", "type": "function", "name": "setApprovalForAll", "inputs": [{"name": "_operator", "type": "address"}, {"name": "_approved", "type": "bool"}], "outputs": [], "gas": 39516}, {"stateMutability": "nonpayable", "type": "function", "name": "mint", "inputs": [{"name": "_to", "type": "address"}, {"name": "_tokenId", "type": "uint256"}, {"name": "token_uri", "type": "string"}], "outputs": [{"name": "", "type": "bool"}], "gas": 189225}, {"stateMutability": "nonpayable", "type": "function", "name": "burn", "inputs": [{"name": "_tokenId", "type": "uint256"}], "outputs": [], "gas": 119991}, {"stateMutability": "view", "type": "function", "name": "name", "inputs": [], "outputs": [{"name": "", "type": "string"}], "gas": 10946}, {"stateMutability": "view", "type": "function", "name": "symbol", "inputs": [], "outputs": [{"name": "", "type": "string"}], "gas": 10976}, {"stateMutability": "view", "type": "function", "name": "tokenURI", "inputs": [{"name": "_tokenId", "type": "uint256"}], "outputs": [{"name": "", "type": "string"}], "gas": 13413}];
    const bridgeAddress = ethers.utils.getAddress("0x72811b6b77d121dccf672dac95fae2f83ab32552");
    const bridgeAbi = [{"name": "Order", "inputs": [{"name": "requester_address", "type": "address", "indexed": true}, {"name": "target_address", "type": "string", "indexed": false}, {"name": "token_address", "type": "address", "indexed": false}, {"name": "token_id", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "Migration", "inputs": [{"name": "migration", "type": "bool", "indexed": false}, {"name": "message", "type": "bytes32", "indexed": true}, {"name": "signatures", "type": "bytes", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "order_migration", "inputs": [{"name": "nft_contract", "type": "address"}, {"name": "token_id", "type": "uint256"}, {"name": "target_account", "type": "string"}], "outputs": [], "gas": 54550}, {"stateMutability": "nonpayable", "type": "function", "name": "cancel_order", "inputs": [{"name": "nft_contract", "type": "address"}, {"name": "token_id", "type": "uint256"}], "outputs": [], "gas": 31282}, {"stateMutability": "nonpayable", "type": "function", "name": "execute_migration", "inputs": [{"name": "original_owner", "type": "address"}, {"name": "nft_contract", "type": "address"}, {"name": "token_id", "type": "uint256"}, {"name": "signatures", "type": "bytes"}], "outputs": [], "gas": 152566}, {"stateMutability": "nonpayable", "type": "function", "name": "unmigrate_token", "inputs": [{"name": "target_owner", "type": "address"}, {"name": "nft_contract", "type": "address"}, {"name": "token_id", "type": "uint256"}, {"name": "signatures", "type": "bytes"}], "outputs": [], "gas": 172103}, {"stateMutability": "view", "type": "function", "name": "get_order_hash", "inputs": [{"name": "original_owner", "type": "address"}, {"name": "nft_contract", "type": "address"}, {"name": "token_id", "type": "uint256"}], "outputs": [{"name": "", "type": "bytes32"}], "gas": 1666}, {"stateMutability": "view", "type": "function", "name": "get_order_sign_hash", "inputs": [{"name": "original_owner", "type": "address"}, {"name": "nft_contract", "type": "address"}, {"name": "token_id", "type": "uint256"}, {"name": "validate", "type": "bool"}], "outputs": [{"name": "", "type": "bytes32"}], "gas": 7418}, {"stateMutability": "view", "type": "function", "name": "get_unmigrate_sign_hash", "inputs": [{"name": "target_owner", "type": "address"}, {"name": "nft_contract", "type": "address"}, {"name": "token_id", "type": "uint256"}], "outputs": [{"name": "", "type": "bytes32"}], "gas": 4501}, {"stateMutability": "view", "type": "function", "name": "signers", "inputs": [{"name": "arg0", "type": "uint256"}], "outputs": [{"name": "", "type": "address"}], "gas": 2775}, {"stateMutability": "view", "type": "function", "name": "required_signatures", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2766}, {"stateMutability": "view", "type": "function", "name": "freezer_period", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2796}, {"stateMutability": "view", "type": "function", "name": "freezer", "inputs": [{"name": "arg0", "type": "bytes32"}], "outputs": [{"name": "", "type": "uint256"}], "gas": 2941}];
    
    const nftContract = new ethers.Contract(nftAddress, nftAbi, provider);
    const nftContractWithSigner = nftContract.connect(signer)
    const bridgeContract = new ethers.Contract(bridgeAddress, bridgeAbi, provider);
    const bridgeContractWithSigner = bridgeContract.connect(signer)

    const txApprove = await nftContractWithSigner.approve(
      bridgeAddress,
      tokenId
    );
    
    console.log("send apporve request", txApprove);
    setTxsOrder([txApprove]);

    const txOrder = await bridgeContractWithSigner.order_migration(
      nftAddress,
      tokenId,
      targetAddress
    )

    setTxsOrder([txApprove, txOrder]);
  } catch (err) {
    setErrorOrder(err.message);
  }
};

const orderUnmigrate = async ({ setErrorUnmigrate, setTxsUnmigrate, tokenId, targetAddress }) => {
  try {
    const available = await TempleWallet.isAvailable();
    if (!available) {
      throw new Error('Thanos Wallet not installed');
    }

    const wallet = new TempleWallet('BridgeApp');
    await wallet.connect('granadanet');
    const Tezos = wallet.toTezos();
    Tezos.setWalletProvider(wallet);
    const selfAddress = Tezos.tz.getAddress;
    await wallet.reconnect('granadanet');

    const tez_nft_address = "KT1TZrzSn39VdRrQvio8j7JZk6mbCta4bRue"
    const contract = await Tezos.wallet.at(tez_nft_address);
    console.log(contract);
    const tx = await contract.methods.request_unmint(
      1,
      targetAddress,
      tokenId,
    ).send({source:selfAddress});
    console.log("tx", tx);

    setTxsUnmigrate([tx.opHash]);
    
  } catch (err) {
    setErrorUnmigrate(err.message);
  }
};

export default function App() {
  const [errorMint, setErrorMint] = useState();
  const [txsMint, setTxsMint] = useState([]);
  const [errorOrder, setErrorOrder] = useState();
  const [txsOrder, setTxsOrder] = useState([]);
  const [errorUnmigrate, setErrorUnmigrate] = useState();
  const [txsUnmigrate, setTxsUnmigrate] = useState([]);
  
  const handleMint = async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    setErrorMint();
    await startMint({
      setErrorMint,
      setTxsMint,
      tokenId: data.get("tokenId"),
      tokenUri: data.get("tokenUri")
    });
  };
  
  const handleOrder = async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    setErrorOrder();
    await orderMigration({
      setErrorOrder,
      setTxsOrder,
      tokenId: data.get("tokenId"),
      targetAddress: data.get("targetAddress")
    });
  };
  
  const handleUnmigrate = async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    setErrorOrder();
    await orderUnmigrate({
      setErrorUnmigrate,
      setTxsUnmigrate,
      tokenId: data.get("tokenId"),
      targetAddress: data.get("targetAddress")
    });
  };
  
  return (
    <Container>
      <form onSubmit={handleMint}>
        <div>
          <h1>
            Mint test token
          </h1>
          <div>
            <input 
              name="tokenId"
              type="text"
              placeholder="Minted token id"
            />
          </div>
          <div>
            <input 
              name="tokenUri"
              type="text"
              placeholder="Minted token uri"
            />
          </div>
          <Button 
            type="submit"
          >
            Mint token
          </Button>
          <ErrorMessage message={errorMint} />
          <TxList txs={txsMint} />
        </div>
      </form>
      <form onSubmit={handleOrder}>
        <div>
          <h1>
            Order migration of the token
          </h1>
          <div>
            <input 
              name="tokenId"
              type="text"
              placeholder="Minted token id"
            />
          </div>
          <div>
            <input 
              name="targetAddress"
              type="text"
              placeholder="tezos target address"
            />
          </div>
          <Button variant="primary" 
            type="submit"
          >
            Order migration
          </Button>
          <ErrorMessage message={errorOrder} />
          <TxList txs={txsOrder} />
        </div>
      </form>
      <form onSubmit={handleUnmigrate}>
        <div>
          <h1>
            Order unmigration of the token
          </h1>
          <div>
            <input 
              name="tokenId"
              type="text"
              placeholder="Tezos token id"
            />
          </div>
          <div>
            <input 
              name="targetAddress"
              type="text"
              placeholder="ethereum target address"
            />
          </div>
          <Button variant="primary"
            type="submit"
          >
            Order unmigrate
          </Button>
          <ErrorMessage message={errorUnmigrate} />
          <TxList txs={txsUnmigrate} />
        </div>
      </form>
    </Container>
  );
}