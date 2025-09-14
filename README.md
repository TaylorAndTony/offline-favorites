## Dependencies

requies `cryptodome` module.

## Workflow

[https://asciiflow.com/#/](https://asciiflow.com/#/)

```
     +---------------------------+         
     |for each file in ./_private|         
     +-------------+-------------+         
                   |                       
                   v                       
      +---------------------------+        
      |    read file content      |        
      +------------+--------------+        
                   |                       
                   v                       
      +----------------------------+       
      | encrypt using AES CBC mode |       
      +------------+---------------+       
                   |                       
                   |                       
+------------------v----------------------+
| add a .enc suffix after original suffix |
+------------------+----------------------+
                   |                       
                   |                       
          +--------v----------+            
          | save to ./_public |            
          +---------+---------+            
                    |                      
                    |                      
            +-------v-------+              
            |  push to git  |              
            +---------------+                          
```

### Encrypt:

```python
def aes_cbc_encrypt(plaintext: str, key: bytes, iv: bytes) -> str:
    """
    使用AES-CBC模式加密数据
    :param plaintext: 待加密的明文（字符串）
    :param key: 加密密钥（必须是16、24或32字节）
    :return: 加密后的密文（base64编码字符串），包含IV
    """
    # 创建AES加密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 对明文进行填充（确保长度是块大小的倍数）并加密
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    # 将IV和密文组合后进行base64编码（IV用于解密）
    return base64.b64encode(ciphertext).decode('utf-8')


def aes_cbc_decrypt(ciphertext_b64: str, key: bytes, iv: bytes) -> str:
    """
    使用AES-CBC模式解密数据
    :param ciphertext_b64: 待解密的密文（base64编码字符串），包含IV
    :param key: 解密密钥（必须与加密密钥相同）
    :return: 解密后的明文（字符串）
    """
    # 解码base64并分离IV和密文
    # 创建AES解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = base64.b64decode(ciphertext_b64)
    # 解密并去除填充
    plaintext = unpad(cipher.decrypt(data), AES.block_size)
    return plaintext.decode('utf-8')

```
### Key management:

key is saved to `key.txt` with the following format:

`{base64 key}.{base64 iv}`

```python
def bytes_to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def base64_to_bytes(data: str) -> bytes:
    return base64.b64decode(data)


class AesKeyManager:
    @staticmethod
    def load_keys_static(filename: str) -> tuple[bytes, bytes]:
        with open(filename, "r", encoding="utf-8") as f:
            k1, k2 = f.read().split(".")
            aes_key = base64_to_bytes(k1)
            iv = base64_to_bytes(k2)
        return aes_key, iv
    
    @staticmethod
    def generate_keys_static() -> tuple[bytes, bytes]:
        aes_key = get_random_bytes(16)
        iv = get_random_bytes(16)
        return aes_key, iv
    
    @staticmethod
    def write_keys_static(filename: str, aes_key: bytes, iv: bytes) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            k1, k2 = bytes_to_base64(aes_key), bytes_to_base64(iv)
            f.write(f"{k1}.{k2}")
```