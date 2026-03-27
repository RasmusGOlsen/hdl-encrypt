from encrypt.parser import HDLLanguage, detect_language, find_protection_blocks


def test_detect_language() -> None:
    assert detect_language("test.v") == HDLLanguage.VERILOG
    assert detect_language("test.sv") == HDLLanguage.VERILOG
    assert detect_language("test.vh") == HDLLanguage.VERILOG
    assert detect_language("test.vhd") == HDLLanguage.VHDL
    assert detect_language("test.vhdl") == HDLLanguage.VHDL
    assert detect_language("unknown.txt") == HDLLanguage.VERILOG


def test_find_protection_blocks_verilog() -> None:
    content = """
module top;
`pragma protect begin
    assign a = b;
`pragma protect end
endmodule
"""
    blocks = find_protection_blocks(content, HDLLanguage.VERILOG)
    assert len(blocks) == 1
    assert blocks[0].content == "assign a = b;"
    assert blocks[0].language == HDLLanguage.VERILOG


def test_find_protection_blocks_vhdl() -> None:
    content = """
entity top is
`protect begin
    a <= b;
`protect end
end entity;
"""
    blocks = find_protection_blocks(content, HDLLanguage.VHDL)
    assert len(blocks) == 1
    assert blocks[0].content == "a <= b;"
    assert blocks[0].language == HDLLanguage.VHDL


def test_find_protection_blocks_vhdl_legacy() -> None:
    content = """
entity top is
-- pragma protect begin
    a <= b;
-- pragma protect end
end entity;
"""
    blocks = find_protection_blocks(content, HDLLanguage.VHDL)
    assert len(blocks) == 1
    assert blocks[0].content == "a <= b;"
    assert blocks[0].language == HDLLanguage.VHDL


def test_find_multiple_blocks() -> None:
    content = """
`pragma protect begin
block1
`pragma protect end
middle
`pragma protect begin
block2
`pragma protect end
"""
    blocks = find_protection_blocks(content, HDLLanguage.VERILOG)
    assert len(blocks) == 2
    assert blocks[0].content == "block1"
    assert blocks[1].content == "block2"
