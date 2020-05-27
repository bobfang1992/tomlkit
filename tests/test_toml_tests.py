import json

import pytest

from tomlkit import parse
from tomlkit._compat import decode, unicode
from tomlkit._utils import parse_rfc3339
from tomlkit.exceptions import TOMLKitError


def to_bool(s):
    assert s in ["true", "false"]

    return s == "true"


stypes = {
    "string": unicode,
    "bool": to_bool,
    "integer": int,
    "float": float,
    "datetime": parse_rfc3339,
}


def untag(value):
    if isinstance(value, list):
        return [untag(i) for i in value]
    elif "type" in value and "value" in value and len(value) == 2:
        if value["type"] in stypes:
            val = decode(value["value"])

            return stypes[value["type"]](val)
        elif value["type"] == "array":
            return [untag(i) for i in value["value"]]
        else:
            raise Exception("Unsupported type {}".format(value["type"]))
    else:
        return {k: untag(v) for k, v in value.items()}


def test_valid_decode(valid_case):
    json_val = untag(json.loads(valid_case["json"]))
    toml_val = parse(valid_case["toml"])

    assert toml_val == json_val
    assert toml_val.as_string() == valid_case["toml"]


def test_invalid_decode(invalid_decode_case):
    with pytest.raises(TOMLKitError):
        parse(invalid_decode_case["toml"])
