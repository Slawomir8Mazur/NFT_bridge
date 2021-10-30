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
    """
    Works for
    0x6c9c5e133b8aafb2ea74f524a5263495e7ae5701c7248805f7b511d973dc7055
    0xadcf97303281a870e48d6e1088ae9a2ead8abd18380452e570d736f628c0460c534790de610d494f9bd7022776a2e246ac63b1216bd0ed8d5fba809aa12b09b81c
    """
    self.signer = self._get_signer(operationHash, signature)
    self.switch = not self.switch
