import base64
import os

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_public_key


def generate_session_key(length: int = 32) -> bytes:
    """Generate a random session key (default 256-bit)."""
    return os.urandom(length)


def encrypt_data(data: bytes, session_key: bytes) -> str:
    """
    Encrypt data using AES-256-CBC.
    Returns base64([IV] + [Ciphertext]).
    """
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(iv + ciphertext).decode("utf-8")


def wrap_session_key(session_key: bytes, public_key_pem: bytes) -> str:
    """
    Wrap the session key using an RSA public key with OAEP padding.
    """
    public_key = load_pem_public_key(public_key_pem)
    if not isinstance(public_key, RSAPublicKey):
        raise ValueError("Provided key is not an RSA public key")
    wrapped_key = public_key.encrypt(
        session_key,
        asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    return base64.b64encode(wrapped_key).decode("utf-8")
