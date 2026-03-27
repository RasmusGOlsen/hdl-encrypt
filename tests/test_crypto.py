import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from encrypt.crypto import encrypt_data, generate_session_key, wrap_session_key


def test_generate_session_key() -> None:
    key = generate_session_key()
    assert len(key) == 32
    assert key != generate_session_key()


def test_encrypt_data() -> None:
    data = b"Hello World"
    key = generate_session_key()
    encrypted = encrypt_data(data, key)
    assert isinstance(encrypted, str)

    # Check if it's valid base64
    decoded = base64.b64decode(encrypted)
    assert len(decoded) > 16  # IV + ciphertext


def test_wrap_session_key() -> None:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    session_key = generate_session_key()
    wrapped = wrap_session_key(session_key, public_key_pem)
    assert isinstance(wrapped, str)

    # Verify wrapping
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

    wrapped_bytes = base64.b64decode(wrapped)
    unwrapped = private_key.decrypt(
        wrapped_bytes,
        asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    assert unwrapped == session_key
