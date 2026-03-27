import sys
from unittest.mock import patch

from encrypt.cli import parse_args


def test_parse_args_basic() -> None:
    test_args = ["prog", "input.v", "-k", "key.pub"]
    with patch.object(sys, "argv", test_args):
        args = parse_args()
        assert args.input == "input.v"
        assert args.key == "key.pub"
        assert args.owner == "Unknown"
        assert args.keyname == "default_key"
        assert not args.full_file


def test_parse_args_all_options() -> None:
    test_args = [
        "prog",
        "input.v",
        "-k",
        "key.pub",
        "-o",
        "out.v",
        "--owner",
        "Me",
        "--keyname",
        "mykey",
        "--full-file",
    ]
    with patch.object(sys, "argv", test_args):
        args = parse_args()
        assert args.input == "input.v"
        assert args.key == "key.pub"
        assert args.output == "out.v"
        assert args.owner == "Me"
        assert args.keyname == "mykey"
        assert args.full_file
