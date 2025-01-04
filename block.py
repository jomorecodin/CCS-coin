import time 
import hashlib
import transaction

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = hash

class Blockchain:
    difficulty = 4

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.mining_reward = 50

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), [], 0, self.calculate_hash(0, "0", int(time.time()), [], 0))

    def calculate_hash(self, index, previous_hash, timestamp, transactions, nonce):
        value = str(index) + previous_hash + str(timestamp) + json.dumps([tx.to_dict() for tx in transactions]) + str(nonce)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address):
        reward_tx = Transaction("0", mining_reward_address, self.mining_reward)
        self.pending_transactions.append(reward_tx)

        latest_block = self.get_latest_block()
        new_index = latest_block.index + 1
        new_timestamp = int(time.time())
        nonce = 0
        new_hash = self.calculate_hash(new_index, latest_block.hash, new_timestamp, self.pending_transactions, nonce)

        while not new_hash.startswith('0' * Blockchain.difficulty):
            nonce += 1
            new_hash = self.calculate_hash(new_index, latest_block.hash, new_timestamp, self.pending_transactions, nonce)

        new_block = Block(new_index, latest_block.hash, new_timestamp, self.pending_transactions, nonce, new_hash)
        self.chain.append(new_block)
        self.pending_transactions = []

     def add_transaction(self, transaction):
        if not transaction.sender or not transaction.recipient or not transaction.amount:
            raise ValueError("Transaction must include sender, recipient, and amount")
        if not transaction.is_valid():
            raise ValueError("Invalid transaction")
        self.pending_transactions.append(transaction)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.transactions, current_block.nonce):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True




    