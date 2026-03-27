from encrypt.formatter import format_ieee1735_block
from encrypt.parser import HDLLanguage


def test_format_ieee1735_block_verilog() -> None:
    encrypted = "ENCRYPTED_DATA"
    wrapped_key = "WRAPPED_KEY"
    formatted = format_ieee1735_block(encrypted, wrapped_key, "Owner", "KeyName", HDLLanguage.VERILOG)
    assert "`pragma protect version = 2" in formatted
    assert "ENCRYPTED_DATA" in formatted
    assert "WRAPPED_KEY" in formatted
    assert 'key_keyowner = "Owner"' in formatted
    assert 'key_keyname = "KeyName"' in formatted


def test_format_ieee1735_block_vhdl() -> None:
    encrypted = "ENCRYPTED_DATA"
    wrapped_key = "WRAPPED_KEY"
    formatted = format_ieee1735_block(encrypted, wrapped_key, "Owner", "KeyName", HDLLanguage.VHDL)
    assert "`protect version = 2" in formatted
    assert "ENCRYPTED_DATA" in formatted
    assert "WRAPPED_KEY" in formatted
    assert 'key_keyowner = "Owner"' in formatted
    assert 'key_keyname = "KeyName"' in formatted
