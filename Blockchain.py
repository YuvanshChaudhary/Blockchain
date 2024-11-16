import json
import hashlib
from cryptography.fernet import Fernet

# Initialize encryption key and cipher
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

# Blockchain block class
class Block:
    def __init__(self, previous_block_hash, transactions):
        self.previous_block_hash = previous_block_hash
        self.transactions = transactions
        self.block_data = "-".join(transactions) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

# Blockchain class to manage blocks
class Blockchain:
    def __init__(self):
        self.chain = []

    def create_genesis_block(self):
        return Block("0", ["Genesis Block"])
        
    def add_block(self, transactions):
        previous_block_hash = self.chain[-1].block_hash if self.chain else "Initial String"
        new_block = Block(previous_block_hash, transactions)
        self.chain.append(new_block)
        print(f"Block added with hash: {new_block.block_hash}")
        print(f"Block data: {new_block.block_data}")

# Initialize the blockchain
blockchain = Blockchain()

# Function to chunk data into smaller parts
def chunk_data(data, chunk_size=1024 * 1024):  # 1 MB chunks
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# Function to simulate storing in decentralized storage (e.g., IPFS)
def store_chunk(chunk):
    # Simulate IPFS hash by hashing the encrypted data chunk
    ipfs_hash = hashlib.sha256(chunk).hexdigest()  # This would be the IPFS hash in a real system
    return ipfs_hash

# Function to handle large data and add to blockchain
def handle_large_data(input_data, blockchain, chunk_size=1024*1024):
    # Split data into chunks and encrypt each chunk
    chunks = chunk_data(input_data.encode(), chunk_size)
    encrypted_chunks = [cipher.encrypt(chunk) for chunk in chunks]
    
    # Store each encrypted chunk, simulate decentralized storage with a hash
    ipfs_hashes = [store_chunk(chunk) for chunk in encrypted_chunks]
    
    # Add each IPFS hash as a transaction to the blockchain
    for i, ipfs_hash in enumerate(ipfs_hashes):
        transaction = {
            "ipfs_hash": ipfs_hash,
            "chunk_order": i,
            "previous_chunk": ipfs_hashes[i - 1] if i > 0 else None
        }
        blockchain.add_block([json.dumps(transaction)])

# Initialize the blockchain
blockchain = Blockchain()

# Main loop to collect data from user
print("Enter data to add to the blockchain. Type 'False' to stop.")
while True:
    user_input = input('Enter Data: ')
    if user_input.lower() == "false":
        break
    handle_large_data(user_input, blockchain)
    
    # Display the current blockchain
    print("\n--- Current Blockchain ---")
    for block in blockchain.chain:
        print(f"Block Hash: {block.block_hash}")
        print(f"Block Data: {block.block_data}")
        print("----")
