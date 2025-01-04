import time

class Transaction:
     def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = int(time.time())
        self.signature = None

    def to_dict(self):
        return OrderedDict({
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        })

    def sign_transaction(self, private_key):
        sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        self.signature = sk.sign(json.dumps(self.to_dict()).encode('utf-8')).hex()

    def is_valid(self):
        if self.sender == "0":  # Mining reward
            return True
        if not self.signature:
            return False
        vk = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)
        return vk.verify(bytes.fromhex(self.signature), json.dumps(self.to_dict()).encode('utf-8'))

    