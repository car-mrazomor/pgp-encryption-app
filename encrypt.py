from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

import os
import base64

def encrypt_b64(original_string):
    byte_data = original_string.encode('utf-8')
    base64_encoded_data = base64.b64encode(byte_data)
    return base64_encoded_data.decode('utf-8')

def decrypt_b64(encoded_string):
    base64_encoded_data = encoded_string.encode('utf-8')
    decoded_data = base64.b64decode(base64_encoded_data)
    return decoded_data.decode('utf-8')

def generate_user_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return public_pem, private_pem

def get_private_public_key(public_pem=None, private_pem=None):
    if public_pem:
        return serialization.load_pem_public_key(public_pem)
    return serialization.load_pem_private_key(private_pem, password=None)

def encrypt_aes(plain_text, aes_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(plain_text.encode()) + encryptor.finalize()
    return iv + encrypted_data

def decrypt_aes(encrypted_data, aes_key):
    iv = encrypted_data[:16]
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
    return decrypted_data.decode()

def encrypt_key(aes_key, public_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

def decrypt_key(encrypted_key, private_key):
    decrypted_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key

def generate_aes_key():
    return os.urandom(32)

def encrypt_data(plain_text, public_key):
    aes_key = generate_aes_key()
    encrypted_data = encrypt_aes(plain_text, aes_key)
    encrypted_key = encrypt_key(aes_key, public_key)
    return base64.b64encode(encrypted_key).decode() + ":" + base64.b64encode(encrypted_data).decode()

def decrypt_data(encrypted_text, private_key):
    encrypted_key_b64, encrypted_data_b64 = encrypted_text.split(":")
    encrypted_key = base64.b64decode(encrypted_key_b64)
    encrypted_data = base64.b64decode(encrypted_data_b64)
    aes_key = decrypt_key(encrypted_key, private_key)
    return decrypt_aes(encrypted_data, aes_key)