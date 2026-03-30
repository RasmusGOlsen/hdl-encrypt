from hdl_encrypt.formatter import format_ieee1735_block
from hdl_encrypt.parser import HDLLanguage


def test_format_ieee1735_block_verilog() -> None:
    encrypted = "ENCRYPTED_DATA"
    wrapped_key = "WRAPPED_KEY"
    keys = [("WRAPPED_KEY", "Owner", "KeyName")]
    formatted = format_ieee1735_block(encrypted, keys, HDLLanguage.VERILOG)
    assert "`pragma protect version = 2" in formatted
    assert "ENCRYPTED_DATA" in formatted
    assert "WRAPPED_KEY" in formatted
    assert 'key_keyowner = "Owner"' in formatted
    assert 'key_keyname = "KeyName"' in formatted


def test_format_ieee1735_block_vhdl() -> None:
    encrypted = "ENCRYPTED_DATA"
    wrapped_key = "WRAPPED_KEY"
    keys = [("WRAPPED_KEY", "Owner", "KeyName")]
    formatted = format_ieee1735_block(encrypted, keys, HDLLanguage.VHDL)
    assert "`protect version = 2" in formatted
    assert "ENCRYPTED_DATA" in formatted
    assert "WRAPPED_KEY" in formatted
    assert 'key_keyowner = "Owner"' in formatted
    assert 'key_keyname = "KeyName"' in formatted
