import re
from dataclasses import dataclass
from enum import Enum


class HDLLanguage(Enum):
    VERILOG = "verilog"
    VHDL = "vhdl"


@dataclass
class ProtectionBlock:
    start_offset: int
    end_offset: int
    content: str
    language: HDLLanguage


def detect_language(filename: str) -> HDLLanguage:
    if filename.endswith((".v", ".sv", ".vh")):
        return HDLLanguage.VERILOG
    if filename.endswith((".vhd", ".vhdl")):
        return HDLLanguage.VHDL
    return HDLLanguage.VERILOG  # Default to Verilog


def find_protection_blocks(content: str, lang: HDLLanguage) -> list[ProtectionBlock]:
    """
    Find blocks of code wrapped in IEEE 1735 protection pragmas.
    """
    if lang == HDLLanguage.VERILOG:
        # Matches `pragma protect begin ... `pragma protect end
        pattern = re.compile(r"`pragma\s+protect\s+begin(.*?)\s+`pragma\s+protect\s+end", re.DOTALL | re.IGNORECASE)
    else:
        # Matches `protect begin ... `protect end
        # Also handle `-- pragma protect begin` for legacy VHDL
        pattern = re.compile(
            r"(?:`|--\s+pragma\s+)protect\s+begin(.*?)\s+(?:`|--\s+pragma\s+)protect\s+end", re.DOTALL | re.IGNORECASE
        )

    blocks = []
    for match in pattern.finditer(content):
        blocks.append(
            ProtectionBlock(
                start_offset=match.start(), end_offset=match.end(), content=match.group(1).strip(), language=lang
            )
        )
    return blocks
