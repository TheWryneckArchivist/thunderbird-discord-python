from thunderbird_workers.worker import MAX_RETRIES


def test_retry_policy_is_positive() -> None:
    assert MAX_RETRIES > 0
