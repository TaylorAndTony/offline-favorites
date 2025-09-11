from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from rich.console import Console
from rich.panel import Panel

import os
import base64

console = Console()

class AESTool:
    def __init__(self, aes_key: bytes | None = None, hmac_key: bytes | None = None):
        self.aes_key = aes_key or get_random_bytes(16)
        self.hmac_key = hmac_key or get_random_bytes(16)

    def save_keys(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            k1, k2 = bytes_to_base64(self.aes_key), bytes_to_base64(self.hmac_key)
            f.write(f"{k1}.{k2}")

    def load_keys(self, filename: str) -> None:
        # with open(filename, "rb") as f:
        #     self.aes_key = f.read(16)
        #     self.hmac_key = f.read(16)
        with open(filename, "r", encoding="utf-8") as f:
            k1, k2 = f.read().split(".")
            self.aes_key = base64_to_bytes(k1)
            self.hmac_key = base64_to_bytes(k2)

    @staticmethod
    def load_keys_static(filename: str) -> tuple[bytes, bytes]:
        # with open(filename, "rb") as f:
        #     aes_key = f.read(16)
        #     hmac_key = f.read(16)
        # return aes_key, hmac_key
        with open(filename, "r", encoding="utf-8") as f:
            k1, k2 = f.read().split(".")
            aes_key = base64_to_bytes(k1)
            hmac_key = base64_to_bytes(k2)
        return aes_key, hmac_key

    def encrypt(self, data: bytes) -> bytes:
        cipher = AES.new(self.aes_key, AES.MODE_CTR)
        ciphertext = cipher.encrypt(data)
        hmac = HMAC.new(self.hmac_key, digestmod=SHA256)
        tag = hmac.update(cipher.nonce + ciphertext).digest()
        return tag + cipher.nonce + ciphertext

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

# Share securely aes_key and hmac_key with the receiver
# encrypted.bin can be sent over an unsecure channel
def ensure_key_existed(filename: str) -> tuple[bytes, bytes]:
    if not os.path.exists(filename):
        aes_key = get_random_bytes(16)
        hmac_key = get_random_bytes(16)
        # console.print(f'AES - key generated: {aes_key.hex()}')
        panel = Panel('Did not find key file, new keys generated to [yellow]./keys.txt[/]', title='[bold red]Warning[/]')
        console.print(panel)
        AESTool(aes_key, hmac_key).save_keys(filename)
        return aes_key, hmac_key
    else:
        aes_key, hmac_key = AESTool.load_keys_static(filename)
        console.print(f'AES - key loaded: {aes_key.hex()}')
        return aes_key, hmac_key
    

def bytes_to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode()

def base64_to_bytes(data: str) -> bytes:
    return base64.b64decode(data)
