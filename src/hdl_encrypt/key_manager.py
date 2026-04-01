import base64
import os
import re
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    load_der_public_key,
    load_pem_public_key,
)


class KeyManager:
    def __init__(self):
        self.keys: dict[str, dict[str, str]] = {}

    def add_key(self, public_key_der: bytes, owner: str, name: str, method: str):
        # Store as base64 string of DER for keying
        key_b64 = base64.b64encode(public_key_der).decode("utf-8")
        # Clean up whitespace/newlines if any
        key_b64 = "".join(key_b64.split())
        self.keys[key_b64] = {
            "owner": owner,
            "name": name,
            "method": method,
            "der": public_key_der,
        }

    def scan_file(self, file_path: str):
        path = Path(file_path)
        if not path.is_file():
            return

        with open(path, "rb") as f:
            content = f.read()

        # Try as PEM first
        try:
            public_key = load_pem_public_key(content)
            if isinstance(public_key, RSAPublicKey):
                der = public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
                self.add_key(der, "Unknown", path.stem, "rsa")
                return
        except Exception:
            pass

        # Try parsing as IEEE 1735 style
        text_content = content.decode("utf-8", errors="ignore")

        # Remove comments to avoid false matches
        text_content = re.sub(r"//.*|--.*", "", text_content)

        # We want to find blocks of metadata and their associated keys.
        # Since the format can be varied (one block per file or multiple),
        # we'll look for key_public_key and then look backwards for metadata
        # or just find all metadata and keys.

        # A better approach: split by toolblocks if present, otherwise treat as one
        blocks = re.split(r"`(?:pragma\s+)?protect\s+(?:begin_toolblock|end_toolblock)", text_content)
        for block in blocks:
            if "key_public_key" not in block:
                continue

            owner_match = re.search(r'key_keyowner\s*=\s*"([^"]+)"', block)
            if not owner_match:
                owner_match = re.search(r'key_keyowner\s*=\s*(\w+)', block)

            name_match = re.search(r'key_keyname\s*=\s*"([^"]+)"', block)
            if not name_match:
                name_match = re.search(r'key_keyname\s*=\s*(\w+)', block)

            method_match = re.search(r'key_method\s*=\s*"([^"]+)"', block)
            if not method_match:
                method_match = re.search(r'key_method\s*=\s*(\w+)', block)

            owner = owner_match.group(1) if owner_match else "Unknown"
            name = name_match.group(1) if name_match else path.stem
            method = method_match.group(1) if method_match else "rsa"

            # Find key_public_key
            public_key_match = re.search(r'key_public_key(?:\s*=\s*)?\s*([A-Za-z0-9+/=\s\n\r]+)', block)
            if public_key_match:
                key_data = public_key_match.group(1).strip()
                lines = key_data.splitlines()
                real_key_lines = []
                for line in lines:
                    clean_line = line.strip()
                    if clean_line.startswith("`") or not clean_line:
                        if real_key_lines: # End of key data
                            break
                        continue
                    # Check if it looks like base64
                    if re.match(r"^[A-Za-z0-9+/=]+$", clean_line):
                        real_key_lines.append(clean_line)
                    else:
                        if real_key_lines:
                            break

                key_b64 = "".join(real_key_lines)
                if key_b64:
                    try:
                        der = base64.b64decode(key_b64)
                        # Validate it's a valid RSA key
                        load_der_public_key(der)
                        self.add_key(der, owner, name, method)
                    except Exception:
                        pass

    def scan_directory(self, dir_path: str):
        path = Path(dir_path)
        if not path.is_dir():
            return

        for file in path.rglob("*"):
            if file.is_file():
                self.scan_file(str(file))

    def scan_env(self, env_var: str = "HDL_ENCRYPT_KEY_PATH"):
        paths = os.environ.get(env_var, "").split(os.pathsep)
        for p in paths:
            if not p:
                continue
            path = Path(p)
            if path.is_dir():
                self.scan_directory(str(path))
            elif path.is_file():
                self.scan_file(str(path))

    def get_keys(self) -> dict[str, dict[str, str]]:
        return self.keys
