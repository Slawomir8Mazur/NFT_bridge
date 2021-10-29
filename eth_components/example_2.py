# @dev Implementation of ERC-20 token standard.
# @author Takayuki Jimba (@yudetamago)
# https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md


owner: public(address)
state: public(bool)

@external
def __init__():
    self.state = True
    self.owner = msg.sender

@internal
def _get_signer(hash: bytes32, v: uint256, r:uint256, s:uint256) -> address:
    return ecrecover(hash, v, r, s)

@external
def swap(operationHash: bytes32, signature: Bytes[65]):
    assert len(signature)==65, "Invalid signature length"
    assert self.owner == self._get_signer(
        operationHash,
        extract32(signature, 0, output_type=uint256),
        extract32(signature, 32, output_type=uint256),
        extract32(signature, 64, output_type=uint256)
    ), "It is not the owner"
    self.state = not self.state
