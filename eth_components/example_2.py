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
def swap(operationHash: bytes32, signature_1: bytes32, signature_2: bytes32, signature_3: bytes32):
    """
    works for params:
    '0xD0a7efE60Fd0850FDc2A63795a4a55460e732f1c'
    '0x1b',
    '0x52e39738034027255b089bbbbc91e9286ae2f01efefa6624285c4d3d509ca0f7', 
    '0x6f217f298e79093e5b51adf2ee5efe29a3f41e6b76e47f58dceae91ce0fac5fb'

    signed by myetherwallet
    """
    self.owner = ecrecover(
        operationHash,
        convert(signature_1, uint256),
        convert(signature_2, uint256),
        convert(signature_3, uint256)
    )
    self.state = not self.state