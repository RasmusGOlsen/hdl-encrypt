from typing import List, Tuple

from .parser import HDLLanguage


def format_ieee1735_block(
    encrypted_data: str, 
    keys: List[Tuple[str, str, str]],  # (wrapped_key, key_owner, key_name)
    lang: HDLLanguage
) -> str:
    prefix = "`pragma " if lang == HDLLanguage.VERILOG else "`"

    lines = [
        f"{prefix}protect version = 2",
        f'{prefix}protect encrypt_agent = "Python IEEE 1735 Encryptor"',
    ]
    
    for wrapped_key, key_owner, key_name in keys:
        lines.extend([
            f'{prefix}protect key_keyowner = "{key_owner}", key_method = "rsa", key_keyname = "{key_name}"',
            f"{prefix}protect key_block",
            wrapped_key,
        ])
    
    lines.extend([
        f'{prefix}protect data_method = "aes256-cbc"',
        f"{prefix}protect data_block",
        encrypted_data,
        f"{prefix}protect end_protected",
    ])

    return "\n".join(lines)
