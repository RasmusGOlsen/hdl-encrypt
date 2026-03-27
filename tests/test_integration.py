from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from encrypt import protect_content
from encrypt.parser import HDLLanguage


def test_protect_content_full_file() -> None:
    private_key = rsa.generate_private_key(65537, 2048)
    public_key_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )

    content = "module top; endmodule"
    protected = protect_content(content, public_key_pem, HDLLanguage.VERILOG, full_file=True)

    assert "`pragma protect data_block" in protected
    assert "module top; endmodule" not in protected


def test_protect_content_inline() -> None:
    private_key = rsa.generate_private_key(65537, 2048)
    public_key_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )

    content = """
module top;
`pragma protect begin
    assign a = b;
`pragma protect end
endmodule
"""
    protected = protect_content(content, public_key_pem, HDLLanguage.VERILOG, full_file=False)

    assert "module top;" in protected
    assert "endmodule" in protected
    assert "`pragma protect data_block" in protected
    assert "assign a = b;" not in protected


def test_protect_content_no_blocks_defaults_to_full() -> None:
    private_key = rsa.generate_private_key(65537, 2048)
    public_key_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )

    content = "module top; endmodule"
    protected = protect_content(content, public_key_pem, HDLLanguage.VERILOG, full_file=False)

    assert "`pragma protect data_block" in protected
    assert "module top; endmodule" not in protected
