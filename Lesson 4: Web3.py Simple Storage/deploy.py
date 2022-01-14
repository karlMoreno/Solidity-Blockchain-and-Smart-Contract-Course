import solcx
from solcx import compile_standard, install_solc

solcx.install_solc("0.6.0")
install_solc("0.6.0")

import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to rinkeby
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/e18d5d4719194f43a95bacd0c71f71fe")) # When accessing ganache from the docker use "HTTP://host.docker.internal:PORT", however when accessing ganache-cli within the docker use given Host:Port
chain_id = 4  # network ID says 5777 but connected node is 1337
my_address = "0x11C0BaF5CC5551e6171b4b272412FBBF0e5127fc" # Remember source .env 
private_key = os.getenv("PRIVATE_KEY")  # add 0x to convert to hexadecimal
# print(private_key)

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest Transaction
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
        
    }
)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract Deployed")

#To work with contract we need
#Contract Address
#Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)

# Call -> Simulate making the call and getting a return value, they do not make a state change
# Transact -> Actually make a state change

#Initial Value of Favorite Number
print(simple_storage.functions.retrieve().call())
print("Updating Contract")

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,

    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())
print('Updated')
