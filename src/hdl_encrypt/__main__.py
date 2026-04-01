import sys
from pathlib import Path

from .cli import parse_args
from .crypto import encrypt_data, generate_session_key, wrap_session_key
from .formatter import format_ieee1735_block
from .key_manager import KeyManager
from .parser import HDLLanguage, detect_language, find_protection_blocks


def protect_content(
    content: str,
    keys_metadata: list[dict[str, any]],
    lang: HDLLanguage,
    full_file: bool = False,
) -> str:
    blocks = find_protection_blocks(content, lang)

    session_key = generate_session_key()

    wrapped_keys = []
    for key_info in keys_metadata:
        wrapped_key = wrap_session_key(session_key, key_info["der"])
        wrapped_keys.append((wrapped_key, key_info["owner"], key_info["name"]))

    if not blocks or full_file:
        # Encrypt the whole file
        encrypted_data = encrypt_data(content.encode("utf-8"), session_key)
        return format_ieee1735_block(encrypted_data, wrapped_keys, lang)
    else:
        # Replace inline blocks
        final_parts = []
        last_offset = 0
        for block in blocks:
            final_parts.append(content[last_offset : block.start_offset])

            encrypted_data = encrypt_data(block.content.encode("utf-8"), session_key)
            formatted_block = format_ieee1735_block(encrypted_data, wrapped_keys, lang)
            final_parts.append(formatted_block)
            last_offset = block.end_offset

        final_parts.append(content[last_offset:])
        return "".join(final_parts)


def main() -> None:
    args = parse_args()

    try:
        with open(args.input) as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    km = KeyManager()

    # 1. Scan from environment variable
    km.scan_env("HDL_ENCRYPT_KEY_PATH")

    # 2. Scan from -k argument
    if args.key:
        path = Path(args.key)
        if path.is_dir():
            km.scan_directory(str(path))
        elif path.is_file():
            km.scan_file(str(path))
        else:
            print(f"Warning: Key path not found: {args.key}")

    keys_dict = km.get_keys()
    if not keys_dict:
        print("Error: No valid public keys found.")
        sys.exit(1)

    # Convert dictionary values to a list for protect_content
    keys_metadata = list(keys_dict.values())

    lang = detect_language(args.input)

    final_content = protect_content(content, keys_metadata, lang, args.full_file)

    output_path = args.output if args.output else f"{args.input}.protected"
    try:
        with open(output_path, "w") as f:
            f.write(final_content)
        print(f"Success! Protected file written to: {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
