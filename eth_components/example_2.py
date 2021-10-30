# @dev Implementation of ERC-20 token standard.
# @author Takayuki Jimba (@yudetamago)
# https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md


owner: public(address)
state: public(bool)

@external
def __init__():
    self.state = True
    self.owner = msg.sender

@external
def swap(operationHash: bytes32, signature: Bytes[65]):
    self.owner = ecrecover(
        operationHash,
        convert(slice(signature, 64, 1), uint256),
        convert(slice(signature, 0, 32), uint256),
        convert(slice(signature, 32, 32), uint256)
    )
    self.state = not self.state