import lib

from rich.console import Console
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

console = Console()

keys: tuple[bytes, bytes] = lib.ensure_key_existed('key.txt')


def aes_cbc_encrypt(plaintext, key, iv):
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


def aes_cbc_decrypt(ciphertext_b64, key, iv):
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

for _ in range(2):
    enc = lib.aes_cbc_encrypt('hello world 872459 jsgdfo-', keys[0], keys[1])
    dec = lib.aes_cbc_decrypt(enc, keys[0], keys[1])
    print(enc)
    print(dec)
