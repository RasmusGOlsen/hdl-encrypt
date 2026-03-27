# IEEE 1735 HDL Encryptor

A Python tool to encrypt HDL (Verilog/VHDL) files following the IEEE 1735 standard.

## Features

- Supports Verilog and VHDL.
- Detects code blocks marked with protection pragmas.
- RSA key-based session key wrapping.
- AES-256-CBC data encryption.
- IEEE 1735 compliant formatting.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### From Source

1. Clone the repository:

   ```bash
   git clone https://github.com/RasmusGOlsen/encrypt.git
   cd encrypt
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

## Usage

You can run the encryptor using `uv run encrypt`:

```bash
uv run encrypt <input_file> -k <public_key_pem> [options]
```

### Arguments

- `input`: The source HDL file (Verilog or VHDL).
- `-k, --key`: Path to the recipient's RSA public key (PEM format).
- `-o, --output`: (Optional) Path to the output file. Defaults to `<input>.protected`.
- `--owner`: (Optional) Key owner name (default: "Unknown").
- `--keyname`: (Optional) Key name (default: "default_key").
- `--full-file`: (Optional) Encrypt the entire file content, ignoring any pragmas.

### Example

```bash
uv run encrypt my_design.v -k company_pub_key.pem -o my_design_protected.v
```

## How it Works

### Protection Pragmas

The tool searches for specific pragmas in your source code to identify which blocks should be encrypted.

**Verilog:**

```verilog
`pragma protect begin
// Your sensitive code here
`pragma protect end
```

**VHDL:**

```vhdl
`protect begin
-- Your sensitive code here
`protect end
```

*Note: VHDL also supports `-- pragma protect begin` style pragmas.*

### Full File Encryption

If no pragmas are found, or if the `--full-file` flag is used, the entire content of the file will be encrypted and wrapped in IEEE 1735 headers.

## Development

### Running Tests

```bash
uv run pytest
```

### Linting and Formatting

```bash
uv run ruff check .
uv run ruff format .
```
