from laborix.http_adapter import HTTPAdapter


def test_http_options_are_explicit() -> None:
    assert HTTPAdapter("http://127.0.0.1", 2, 1).request_options() == {
        "endpoint": "http://127.0.0.1",
        "timeout": 2,
        "retries": 1,
    }
