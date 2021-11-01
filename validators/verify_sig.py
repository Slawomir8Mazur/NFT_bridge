import web3

message = bytes.fromhex("6c9c5e133b8aafb2ea74f524a5263495e7ae5701c7248805f7b511d973dc7055")
signature = bytes.fromhex("adcf97303281a870e48d6e1088ae9a2ead8abd18380452e570d736f628c0460c534790de610d494f9bd7022776a2e246ac63b1216bd0ed8d5fba809aa12b09b81c")

recovered_hash = web3.eth.Account.recoverHash(message, signature=signature)

print(recovered_hash)