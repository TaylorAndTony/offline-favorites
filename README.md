## Encryption

requies `cryptodome` module.

### Encrypt:

```python
def __init__(self, aes_key: bytes | None = None, hmac_key: bytes | None = None):
    self.aes_key = aes_key or get_random_bytes(16)
    self.hmac_key = hmac_key or get_random_bytes(16)


def encrypt(self, data: bytes) -> bytes:
    cipher = AES.new(self.aes_key, AES.MODE_CTR)
    ciphertext = cipher.encrypt(data)
    hmac = HMAC.new(self.hmac_key, digestmod=SHA256)
    tag = hmac.update(cipher.nonce + ciphertext).digest()
    return tag + cipher.nonce + ciphertext
```

### Decrypt:

```python
def decrypt(self, data: bytes) -> bytes | None:
    tag = data[:32]
    nonce = data[32:40]
    ciphertext = data[40:]
    try:
        hmac = HMAC.new(self.hmac_key, digestmod=SHA256)
        hmac.update(nonce + ciphertext)
        hmac.verify(tag)
    except ValueError:
        print("The message was modified!")
        return None
    cipher = AES.new(self.aes_key, AES.MODE_CTR, nonce=nonce)
    message = cipher.decrypt(ciphertext)
    return message
```