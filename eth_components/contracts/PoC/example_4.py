signers: public(address[5])
required_signatures: public(uint256)
message: public(bytes32)

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
    self.message = empty(bytes32)


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
def change_signer(message: bytes32, signatures: Bytes[65*5]):
    valid_signatures: uint256 = self._get_valid_signers_count(message, signatures)
    assert valid_signatures >= self.required_signatures, "You provided to few valid signatures"
    self.message = message
