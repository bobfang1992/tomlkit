from __future__ import unicode_literals

from tomlkit import dumps, loads


def test_write_backslash():
    d = {"foo": "\e\u25E6\r"}  # noqa: W605

    expected = """foo = "\\\\e\u25E6\\r"
"""

    assert expected == dumps(d)
    assert loads(dumps(d))["foo"] == "\e\u25E6\r"  # noqa: W605
