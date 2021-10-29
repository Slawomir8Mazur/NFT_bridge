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
def swap():
    assert msg.sender == self.owner
    self.state = not self.state
