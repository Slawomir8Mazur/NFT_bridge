# DOesn't work, can't pass array as input via MEW interface, 

store: public(bytes32[2])

@external
def __init__():
    self.store = [0x06d8cb9bc99d787b486478b78450871782a36b76edc198c3477e893043d99cc5, 0x06d8cb9bc99d787b486478b78450871782a36b76edc198c3477e893043d99cc6]

@external
def update_store(store: bytes32[2]):
    self.store = store

@external
def update_single_store(store: bytes32):
    self.store[0] = store
    self.store[1] = store
