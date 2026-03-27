import sys

from .cli import parse_args
from .crypto import encrypt_data, generate_session_key, wrap_session_key
from .formatter import format_ieee1735_block
from .parser import HDLLanguage, detect_language, find_protection_blocks


def protect_content(
    content: str,
    public_key_pem: bytes,
    lang: HDLLanguage,
    owner: str = "Unknown",
    keyname: str = "default_key",
    full_file: bool = False,
) -> str:
    blocks = find_protection_blocks(content, lang)

    session_key = generate_session_key()
    wrapped_key = wrap_session_key(session_key, public_key_pem)

    if not blocks or full_file:
        # Encrypt the whole file
        encrypted_data = encrypt_data(content.encode("utf-8"), session_key)
        return format_ieee1735_block(encrypted_data, wrapped_key, owner, keyname, lang)
    else:
        # Replace inline blocks
        final_parts = []
        last_offset = 0
        for block in blocks:
            final_parts.append(content[last_offset : block.start_offset])

            encrypted_data = encrypt_data(block.content.encode("utf-8"), session_key)
            formatted_block = format_ieee1735_block(encrypted_data, wrapped_key, owner, keyname, lang)
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

    try:
        with open(args.key, "rb") as f:
            public_key_pem = f.read()
    except Exception as e:
        print(f"Error reading key file: {e}")
        sys.exit(1)

    lang = detect_language(args.input)

    final_content = protect_content(content, public_key_pem, lang, args.owner, args.keyname, args.full_file)

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
