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
    Works for:
    message= 0x6c9c5e133b8aafb2ea74f524a5263495e7ae5701c7248805f7b511d973dc7055
    signature= 0xadcf97303281a870e48d6e1088ae9a2ead8abd18380452e570d736f628c0460c534790de610d494f9bd7022776a2e246ac63b1216bd0ed8d5fba809aa12b09b81c

    message= 0x5bf1e3244d63b4a4126a055fdd1c046bc464b657d1f24c29dcb56d4a7d0b48ec
    signature= 0x8a2aebd2323e6a0548869f82989059213ba15b84422003725260ec52aeae04a11a5937b415b2e0ec3d4252f9d87c7b0cd811e5ec86c3b08124c74f57ff749e9e1c
    """
    self.signer = self._get_signer(operationHash, signature)
    self.switch = not self.switch
