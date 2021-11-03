### Scenario 1

#### Desciption

* user account: 0x291Eea42f2806d7b5f14C5e71f3a97b0a5Bcf62e
* erc-721 account: 0x5036bf1c86b03dc74bcf490ea5fbad4426069069
* token with id 21 was minted in erc-721 contract, user set as owner
* main contract deployed at 0x313309192D561C99563e8cEDcACd8a1655b73879 
* call order_migration with 0x5036bf1c86b03dc74bcf490ea5fbad4426069069, 21, 0x747a3157487970615735684268625355744b7175746b44745465354a6944434c53704446
* call get_order_hash with 0x291Eea42f2806d7b5f14C5e71f3a97b0a5Bcf62e, 0x5036bf1c86b03dc74bcf490ea5fbad4426069069, 21: received 0xa04f8cb4209134f3655c38b889d4bd4f98ba20cb3c4c7f85f74dc16c805633c4
* call freezer with 0xa04f8cb4209134f3655c38b889d4bd4f98ba20cb3c4c7f85f74dc16c805633c4: received 1635894137
* call get_order_sign_hash with 0x291Eea42f2806d7b5f14C5e71f3a97b0a5Bcf62e, 0x5036bf1c86b03dc74bcf490ea5fbad4426069069, 21, False:
0x79d803cb4672e9bb1626b02d93c2c0e73f5139ffd1e737743ed2981f416d4d8f
* call execute_migration with 0x291Eea42f2806d7b5f14C5e71f3a97b0a5Bcf62e, 0x5036bf1c86b03dc74bcf490ea5fbad4426069069, 21, 0xda93309f44292a4658cbd4f2a72ce006c784134e00faddbf809ea45d8df346d1328bce2ab0f58359283f288910584bd515e88e18dc3dd490a7685bb1291bd3491c4bb405e04d411a6be58580092f2554b7410c95b566c1a9091dabaded3101d0fd2138e9ad76a0d5704fd8523246587bcfde5f8d4d033a0ecec8ecbab8e19b017a1c (comment: should fail, only two signatures here)
* call execute_migration with 0x291Eea42f2806d7b5f14C5e71f3a97b0a5Bcf62e, 0x5036bf1c86b03dc74bcf490ea5fbad4426069069, 21, 0xbcf60d19b84feecb0eed8efec375ba4caa8a48efd8c86bc9efe447bd9bbea4612191da1535932f9655aa5e85239b50d056a221e6a8502b2112344e51a85313f41bc45724ae5bc3897b227c12982dfb18b8586e454e44a1bc4a1f7bcfd35be7cbe93a9be55e6fbb431fc5a4166f6a90fb00317df5032fe0af2e7c821a492cdf12771c357fa63c378b6cd65c74a7adb114f3481368a4a6c95230ea2f28bd17b9b317812aa866db08b9c4c0f1e91bd3a7a4f3dc4e68fae98a37122c7279041a11693e8c1c4cf4ee49e81dcd9dab9122e2bed421ded794413655e85219c3e3d98899cf0cf1676afbef6672b24347c4fabf3f879eef5f7604316e2f30af38e504e359b831b21b2bd150e1d4b9e19a322529d4ad67bab6d6f5ff9b46410ebdbd4fedee65b0d80057ac22c33b1e66e516dd9fff07ff3a09e1b39bcfba09a36d704b0437106abefc1b (comment: should fail, erc-721 are not allowed yet) execution reverted
* call approve in 0x5036bf1c86b03dc74bcf490ea5fbad4426069069 with 0x313309192D561C99563e8cEDcACd8a1655b73879
* call execute_migration with 0x291Eea42f2806d7b5f14C5e71f3a97b0a5Bcf62e, 0x5036bf1c86b03dc74bcf490ea5fbad4426069069, 21, 0xbcf60d19b84feecb0eed8efec375ba4caa8a48efd8c86bc9efe447bd9bbea4612191da1535932f9655aa5e85239b50d056a221e6a8502b2112344e51a85313f41bc45724ae5bc3897b227c12982dfb18b8586e454e44a1bc4a1f7bcfd35be7cbe93a9be55e6fbb431fc5a4166f6a90fb00317df5032fe0af2e7c821a492cdf12771c357fa63c378b6cd65c74a7adb114f3481368a4a6c95230ea2f28bd17b9b317812aa866db08b9c4c0f1e91bd3a7a4f3dc4e68fae98a37122c7279041a11693e8c1c4cf4ee49e81dcd9dab9122e2bed421ded794413655e85219c3e3d98899cf0cf1676afbef6672b24347c4fabf3f879eef5f7604316e2f30af38e504e359b831b21b2bd150e1d4b9e19a322529d4ad67bab6d6f5ff9b46410ebdbd4fedee65b0d80057ac22c33b1e66e516dd9fff07ff3a09e1b39bcfba09a36d704b0437106abefc1b

#### Summary

* tests passed
* `migration` functionality works for the ethereum part
* other test simulating attack on contract should be undertaken 