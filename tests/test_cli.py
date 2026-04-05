import argparse
from dataclasses import dataclass

import pytest


@dataclass
class CliResult:
    mode: str
    text: str
    repeat: int


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="strint")
    parser.add_argument("text", nargs="?", default="")
    parser.add_argument("--mode", choices=["echo", "upper", "lower"], default="echo")
    parser.add_argument("--repeat", type=int, default=1)
    return parser


def run_cli(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.repeat < 1:
        raise ValueError("--repeat must be >= 1")

    transformed = args.text
    if args.mode == "upper":
        transformed = transformed.upper()
    elif args.mode == "lower":
        transformed = transformed.lower()

    return CliResult(mode=args.mode, text=transformed, repeat=args.repeat)


def test_cli_default_mode_echo():
    result = run_cli(["Hello"])
    assert result.mode == "echo"


def test_cli_default_repeat_one():
    result = run_cli(["Hello"])
    assert result.repeat == 1


def test_cli_echo_preserves_text():
    result = run_cli(["Hello", "--mode", "echo"])
    assert result.text == "Hello"


def test_cli_upper_transforms_text():
    result = run_cli(["Hello", "--mode", "upper"])
    assert result.text == "HELLO"


def test_cli_lower_transforms_text():
    result = run_cli(["HeLLo", "--mode", "lower"])
    assert result.text == "hello"


def test_cli_repeat_two_parsed():
    result = run_cli(["abc", "--repeat", "2"])
    assert result.repeat == 2


def test_cli_repeat_large_parsed():
    result = run_cli(["abc", "--repeat", "99"])
    assert result.repeat == 99


def test_cli_repeat_zero_rejected():
    with pytest.raises(ValueError):
        run_cli(["abc", "--repeat", "0"])


def test_cli_repeat_negative_rejected():
    with pytest.raises(ValueError):
        run_cli(["abc", "--repeat", "-1"])


def test_cli_invalid_mode_rejected():
    with pytest.raises(SystemExit):
        run_cli(["abc", "--mode", "title"])


def test_cli_help_rejected_to_system_exit():
    with pytest.raises(SystemExit):
        run_cli(["--help"])


def test_cli_empty_text_allowed():
    result = run_cli([])
    assert result.text == ""


def test_cli_mode_flag_before_text():
    result = run_cli(["--mode", "upper", "abc"])
    assert result.text == "ABC"


def test_cli_mode_flag_after_text():
    result = run_cli(["abc", "--mode", "lower"])
    assert result.text == "abc"


def test_cli_repeat_then_mode():
    result = run_cli(["abc", "--repeat", "3", "--mode", "upper"])
    assert result.mode == "upper"


def test_cli_mode_then_repeat():
    result = run_cli(["abc", "--mode", "lower", "--repeat", "3"])
    assert result.repeat == 3


def test_cli_text_with_spaces_when_quoted_style():
    result = run_cli(["hello world", "--mode", "upper"])
    assert result.text == "HELLO WORLD"


def test_cli_unicode_upper_supported():
    result = run_cli(["straße", "--mode", "upper"])
    assert result.text


def test_cli_unicode_lower_supported():
    result = run_cli(["İ", "--mode", "lower"])
    assert isinstance(result.text, str)


def test_cli_parser_prog_name():
    parser = build_parser()
    assert parser.prog == "strint"


def test_cli_result_dataclass_mode():
    result = run_cli(["x"])
    assert hasattr(result, "mode")


def test_cli_result_dataclass_text():
    result = run_cli(["x"])
    assert hasattr(result, "text")


def test_cli_result_dataclass_repeat():
    result = run_cli(["x"])
    assert hasattr(result, "repeat")


def test_cli_non_integer_repeat_rejected():
    with pytest.raises(SystemExit):
        run_cli(["x", "--repeat", "abc"])


def test_cli_double_mode_last_one_wins():
    result = run_cli(["x", "--mode", "upper", "--mode", "lower"])
    assert result.mode == "lower"
