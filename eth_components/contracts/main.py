from vyper.interfaces import ERC721

struct NftFrozen:
    token_address: address
    token_id: uint256
    original_owner: address

# Setup signatures
signers: public(address[5])
required_signatures: public(uint256)

# Setup freezing 
freezer_period: public(uint256) # timedelta
freezer: public(HashMap[bytes32, uint256])
    # [keccak256(concat(
    #     convert(msg.sender, bytes32),
    #     convert(nft_contract, bytes32),
    #     convert(token_id, bytes32)
    # )), frozen_until=timestamp]


@external
def __init__():
    self.signers = [
        0xD0a7efE60Fd0850FDc2A63795a4a55460e732f1c,
        0x66665824128f77Cc2b722A5768914131312e4dC4,
        0x4b3899157921035c76dac469101663ff34Dbc992,
        0xdba01494fe398c5387fA1EDa3D6098364C99F7c5,
        0x0DE1F8Aa263E642ec8932FE15076f829295fA464
    ]
    self.required_signatures = 3
    self.freezer_period = 1000
    # self.para = Pair({x: 122, y:44})


@internal
def _get_signer(message: bytes32, signature: Bytes[65]) -> address:
    return ecrecover(
        message,
        convert(slice(signature, 64, 1), uint256),
        convert(slice(signature, 0, 32), uint256),
        convert(slice(signature, 32, 32), uint256)
    )


@internal
def _get_valid_signers_count(message: bytes32, signatures: Bytes[65*5]) -> uint256:
    # Verify signatures, deduplicate them
    received_signatures: uint256 = len(signatures)/65
    tmp_addresses: address[5] = empty(address[5])

    for i in range(5):
        if i >= received_signatures:
            break
        signature: Bytes[65] = slice(signatures, 65*i, 65)
        tmp_addresses[i] = self._get_signer(message, signature)
    
    # Count signatures from allowed signers
    confirmation_counter: uint256 = 0
    for signer in self.signers:
        if signer in tmp_addresses:
            confirmation_counter += 1
    return confirmation_counter

@external
def safe_order_migration(nft_contract: address, token_id: uint256):
    """
        User requests his NFT token on ethereum to be megrated to Tezos, 
        order is recorded in the freezer, it will either be: 
        1. minted on tezos and here it will be removed from freezer - this 
        contract will become a owner of the token
        2. minters will do nothing about it, user will be able to withdraw 
        it after freezing period (up to one hour, it saves us from errors 
        from racing conditions).
    """
    self.freezer[keccak256(concat(
        convert(msg.sender, bytes32),
        convert(nft_contract, bytes32),
        convert(token_id, bytes32)
    ))] = block.timestamp + self.freezer_period
    # self.para = Pair({x: 122, y:44})
    # ERC721(nft_address).transferFrom(msg.sender, self, token_id)


@external
def execute_migration(original_owner: address, nft_contract: address, token_id: uint256, signatures: Bytes[65*5]):
    """
        Minters are minting nft ordered for migration on Tezos, here we will 
        also transfer nft to this contract and remove it from the freezer
    """
    order_hash: bytes32 = keccak256(concat(
        convert(msg.sender, bytes32),
        convert(nft_contract, bytes32),
        convert(token_id, bytes32)
    ))
    assert self.required_signatures <= self._get_valid_signers_count(order_hash, signatures), "Too few valid signatures"

    # Remove order from freezer
    self.freezer[order_hash] = empty(uint256)

    # Transfer NFT to this contract
    ERC721(nft_contract).transferFrom(original_owner, self, token_id)


@external
def cancel_order(original_owner: address, nft_contract: address, token_id: uint256):
    """
        User can cancel order if minters weren't able to 
        fulfill it in configured timespan
    """
    order_hash: bytes32 = keccak256(concat(
        convert(msg.sender, bytes32),
        convert(nft_contract, bytes32),
        convert(token_id, bytes32)
    ))
    freezing_period: uint256 = self.freezer[order_hash]
    assert freezing_period != 0, "There was no order for your parameters"
    assert freezing_period <= block.timestamp, "Freezing period didn't end for that order yet"

    # Remove order from the freezer
    self.freezer[order_hash] = empty(uint256)
