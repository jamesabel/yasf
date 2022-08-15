from yasf import sf, structured_sentinel, escaped_structured_sentinel, sf_separate


def test_sentinel():
    message = f"a {structured_sentinel} here"
    out = sf(message, number=42, funny_string=f"funny {structured_sentinel}")
    print(out)
    args, kwargs = sf_separate(out)
    assert args == f"a {escaped_structured_sentinel} here"  # we don't try to remove the escaped sentinel
    assert kwargs == '{"number": 42, "funny_string": "funny ' + escaped_structured_sentinel + '"}'
