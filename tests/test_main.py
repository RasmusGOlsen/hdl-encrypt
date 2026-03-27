import pathlib
import sys
from unittest.mock import MagicMock, patch

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from encrypt import main


def test_main_success(tmp_path: pathlib.Path) -> None:
    # Setup RSA key
    private_key = rsa.generate_private_key(65537, 2048)
    public_key_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )

    key_file = tmp_path / "key.pub"
    key_file.write_bytes(public_key_pem)

    input_file = tmp_path / "input.v"
    input_file.write_text("module top; endmodule")

    output_file = tmp_path / "output.v"

    test_args = ["encrypt", str(input_file), "-k", str(key_file), "-o", str(output_file)]

    with patch.object(sys, "argv", test_args):
        with patch("builtins.print") as mock_print:
            main()
            mock_print.assert_any_call(f"Success! Protected file written to: {output_file}")

    assert output_file.exists()
    assert "`pragma protect data_block" in output_file.read_text()


def test_main_default_output(tmp_path: pathlib.Path) -> None:
    # Setup RSA key
    private_key = rsa.generate_private_key(65537, 2048)
    public_key_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )

    key_file = tmp_path / "key.pub"
    key_file.write_bytes(public_key_pem)

    input_file = tmp_path / "input.v"
    input_file.write_text("module top; endmodule")

    expected_output = tmp_path / "input.v.protected"

    test_args = ["encrypt", str(input_file), "-k", str(key_file)]

    with patch.object(sys, "argv", test_args):
        with patch("builtins.print") as mock_print:
            main()
            mock_print.assert_any_call(f"Success! Protected file written to: {expected_output}")

    assert expected_output.exists()


def test_main_input_read_error() -> None:
    test_args = ["encrypt", "nonexistent.v", "-k", "key.pub"]
    with patch.object(sys, "argv", test_args):
        with patch("builtins.open", side_effect=Exception("Read Error")):
            with patch("builtins.print") as mock_print:
                with patch("sys.exit", side_effect=SystemExit) as mock_exit:
                    import pytest

                    with pytest.raises(SystemExit):
                        main()
                    mock_print.assert_any_call("Error reading input file: Read Error")
                    mock_exit.assert_called_with(1)


def test_main_key_read_error(tmp_path: pathlib.Path) -> None:
    input_file = tmp_path / "input.v"
    input_file.write_text("module top; endmodule")

    test_args = ["encrypt", str(input_file), "-k", "nonexistent.pub"]
    with patch.object(sys, "argv", test_args):
        # First open for input works, second for key fails
        def side_effect(path: str | pathlib.Path, mode: str = "r") -> MagicMock:
            if "input.v" in str(path):
                from typing import cast
                from unittest.mock import mock_open

                return cast(MagicMock, mock_open(read_data="content").return_value)
            raise Exception("Key Error")

        with patch("builtins.open", side_effect=side_effect):
            with patch("builtins.print") as mock_print:
                with patch("sys.exit", side_effect=SystemExit) as mock_exit:
                    import pytest

                    with pytest.raises(SystemExit):
                        main()
                    mock_print.assert_any_call("Error reading key file: Key Error")
                    mock_exit.assert_called_with(1)


def test_main_write_error(tmp_path: pathlib.Path) -> None:
    # Setup RSA key
    private_key = rsa.generate_private_key(65537, 2048)
    public_key_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )

    key_file = tmp_path / "key.pub"
    key_file.write_bytes(public_key_pem)

    input_file = tmp_path / "input.v"
    input_file.write_text("module top; endmodule")

    test_args = ["encrypt", str(input_file), "-k", str(key_file), "-o", "/forbidden/output.v"]

    with patch.object(sys, "argv", test_args):
        with patch("builtins.print") as mock_print:
            with patch("sys.exit", side_effect=SystemExit) as mock_exit:
                import pytest

                with pytest.raises(SystemExit):
                    main()
                # The error message depends on OS, but it should start with "Error writing output file"
                args, _ = mock_print.call_args
                assert args[0].startswith("Error writing output file:")
                mock_exit.assert_called_with(1)
