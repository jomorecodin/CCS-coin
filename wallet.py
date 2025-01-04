def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1).to_string().hex()
        self.public_key = SigningKey.from_string(bytes.fromhex(self.private_key), curve=SECP256k1).verifying_key.to_string().hex()

    def get_address(self):
        return self.public_key
