# @dev Implementation of ERC-20 token standard.
# @author Takayuki Jimba (@yudetamago)
# https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md


owner: public(address)
signer: public(address)
switch: public(bool)

@external
def __init__():
    self.switch = True
    self.owner = msg.sender
    self.signer = msg.sender


@internal
def _get_signer(operationHash: bytes32, signature: Bytes[65]) -> address:
    return ecrecover(
        operationHash,
        convert(slice(signature, 64, 1), uint256),
        convert(slice(signature, 0, 32), uint256),
        convert(slice(signature, 32, 32), uint256)
    )

@external
def change_signer(operationHash: bytes32, signature: Bytes[65]):
    self.signer = self._get_signer(operationHash, signature)
    self.switch = not self.switch
