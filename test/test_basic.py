from chats import token_utils


def test_basic():
    count = token_utils.count_tokens("Hello World")
    assert count == 2
