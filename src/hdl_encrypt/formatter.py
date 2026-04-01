from ._version import __version__
from .parser import HDLLanguage


def format_ieee1735_block(
    encrypted_data: str,
    keys: list[tuple[str, str, str]],  # (wrapped_key, key_owner, key_name)
    lang: HDLLanguage
) -> str:
    prefix = "`pragma " if lang == HDLLanguage.VERILOG else "`"

    lines = [
        f"{prefix}protect begin_protected",
        f"{prefix}protect version = 1",
        f'{prefix}protect encrypt_agent = "HDL Encrypt", encrypt_agent_info = "{__version__}"',
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
