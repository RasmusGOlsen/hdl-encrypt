import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="IEEE 1735 HDL Encryptor")
    parser.add_argument("input", help="Input HDL file (Verilog/VHDL)")
    parser.add_argument("-k", "--key", required=True, help="Path to RSA public key (PEM)")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--owner", default="Unknown", help="Key owner name")
    parser.add_argument("--keyname", default="default_key", help="Key name")
    parser.add_argument("--full-file", action="store_true", help="Encrypt full file regardless of pragmas")

    return parser.parse_args()
