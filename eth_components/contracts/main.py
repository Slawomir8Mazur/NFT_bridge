from vyper.interfaces import ERC721

event Order:
    requester_address: indexed(address)
    target_address: Bytes[36]
    token_address: address
    token_id: uint256

event Migration:
    migration: bool # True for migration, False for unmigration
    message: indexed(bytes32)
    signatures: Bytes[325]

# Setup signatures
signers: public(address[5])
required_signatures: public(uint256)

# Setup freezing 
freezer_period: public(uint256) # timedelta
freezer: public(HashMap[bytes32, uint256])
# >>> 0xedc905c6150a64657f27b89836c75ff42924c311ba766e04f12b9169a586ae1c
# 1635801289

_unmigrate_counter: uint256


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
    self.freezer_period = 3600
    self._unmigrate_counter = 0

################# PRIVATE METHODS ######################

@view
@internal
def _get_signer(message: bytes32, signature: Bytes[65]) -> address:
    return ecrecover(
        message,
        convert(slice(signature, 64, 1), uint256),
        convert(slice(signature, 0, 32), uint256),
        convert(slice(signature, 32, 32), uint256)
    )

@view
@internal
def _get_valid_signers_count(message: bytes32, signatures: Bytes[325]) -> uint256:
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

@view
@internal
def _create_order_hash(owner: address, nft_contract: address, token_id: uint256) -> bytes32:
    return keccak256(concat(
        convert(owner, bytes32),
        convert(nft_contract, bytes32),
        convert(token_id, bytes32)
    ))

@view
@internal
def _create_order_sign_hash(order_hash: bytes32, nonce: uint256) -> bytes32:
    return keccak256(concat(
        order_hash,
        convert(nonce, bytes32)
    ))

######################### USER METHODS ##################################

@external
def order_migration(nft_contract: address, token_id: uint256, target_account: Bytes[36]):
    """
    User requests his NFT token on ethereum to be megrated to Tezos, 
    order is recorded in the freezer, it will either be: 
    1. minted on tezos and here it will be removed from freezer - this 
    contract will become a owner of the token
    2. minters will do nothing about it, user will be able to withdraw 
    it after freezing period (up to one hour, it saves us from errors 
    from racing conditions).
    >>> nft_contract, token_id, target_account ='0x90df8a8ff585d1eb4b9a13789bcc5fd8c7e1b7b2', 18, '0x747a3157487970615735684268625355744b7175746b44745465354a6944434c53704446'
    """
    order_hash: bytes32 = self._create_order_hash(msg.sender, nft_contract, token_id)
    self.freezer[order_hash] = block.timestamp
    log Order(msg.sender, target_account, nft_contract, token_id)

@external
def cancel_order(nft_contract: address, token_id: uint256):
    """
    User can cancel order if minters weren't able to 
    fulfill it in configured timespan
    """
    order_hash: bytes32 = self._create_order_hash(msg.sender, nft_contract, token_id)
    add_time: uint256 = self.freezer[order_hash]
    assert add_time != 0, "There was no order for your parameters"
    assert add_time + self.freezer_period >= block.timestamp, "Freezing period didn't end for that order yet"

    # Remove order from the freezer
    self.freezer[order_hash] = empty(uint256)

######################### VALIDATORS METHODS ##################################

@external
def execute_migration(original_owner: address, nft_contract: address, token_id: uint256, signatures: Bytes[325]):
    """
    Token is removed from the freezer, validators confirm with their signatures that they 
    minted that token on other blockchain, migration can be undone by the seperate procedure 
    started on other blockchain, freezer no longer applies - user can unmint upon request    
    """
    order_hash: bytes32 = self._create_order_hash(original_owner, nft_contract, token_id)

    add_time: uint256 = self.freezer[order_hash]
    assert add_time != empty(uint256), "There was no such an order"
    assert add_time + self.freezer_period > block.timestamp, "Migration wasn't establised in dued time"

    order_sign_hash: bytes32 = self._create_order_sign_hash(order_hash, add_time)
    assert self.required_signatures <= self._get_valid_signers_count(order_sign_hash, signatures), "Too few valid signatures"

    # Remove order from freezer
    self.freezer[order_hash] = empty(uint256)

    # Transfer NFT to this contract
    ERC721(nft_contract).transferFrom(original_owner, self, token_id)

    log Migration(True, order_sign_hash, signatures)


@external
def unmigrate_token(target_owner: address, nft_contract: address, token_id: uint256, signatures: Bytes[325]):
    """
    User initiated unmigrating procedure on other blockchain, if it was accepted by validators there, 
    then here validators should provide their signatures as confirmation - token will be transfered to requested user
    """
    order_hash: bytes32 = self._create_order_hash(target_owner, nft_contract, token_id)
    order_sign_hash: bytes32 = self._create_order_sign_hash(order_hash, self._unmigrate_counter)
    assert self.required_signatures <= self._get_valid_signers_count(order_sign_hash, signatures), "Too few valid signatures"

    self._unmigrate_counter += 1
    ERC721(nft_contract).transferFrom(self, target_owner, token_id)

    log Migration(False, order_sign_hash, signatures)

############################ VIEWS ############################

@view
@external
def get_order_hash(original_owner: address, nft_contract: address, token_id: uint256) -> bytes32:
    """
    >>> original_owner, nft_contract, token_id ='0x291eea42f2806d7b5f14c5e71f3a97b0a5bcf62e', '0x90df8a8ff585d1eb4b9a13789bcc5fd8c7e1b7b2', 21
    0xedc905c6150a64657f27b89836c75ff42924c311ba766e04f12b9169a586ae1c
    """
    return self._create_order_hash(original_owner, nft_contract, token_id)

@view
@external
def get_order_sign_hash(original_owner: address, nft_contract: address, token_id: uint256, validate: bool) -> bytes32:
    """
    Return hash calculated from: 
    * `get_order_hash` for token and user ordering migration
    * nonce that for this function is timestamp when user created an order
    Function `execute_migration` can only be executed when signatures do sign hash of `this` function 
    """
    order_hash: bytes32 = self._create_order_hash(original_owner, nft_contract, token_id)

    add_time: uint256 = self.freezer[order_hash]

    if validate:
        assert add_time != empty(uint256), "There was no such an order"
        assert add_time + self.freezer_period > block.timestamp, "Migration wasn't establised in dued time"

    return self._create_order_sign_hash(order_hash, add_time)

@view
@external
def get_unmigrate_sign_hash(target_owner: address, nft_contract: address, token_id: uint256) -> bytes32:
    """
    Return hash calculated from: 
    * `get_order_hash` for token and user ordering migration
    * nonce that for this function is `_unmigrate_counter`
    Function `unmigrate_token` can only be executed when signatures do sign hash of `this` function 
    """
    order_hash: bytes32 = self._create_order_hash(target_owner, nft_contract, token_id)
    return self._create_order_sign_hash(order_hash, self._unmigrate_counter)