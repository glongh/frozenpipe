from ratelimiter.bucket import Bucket
import time
import pytest


class FakeTimer():
    """
    A fake timer to test against time
    """

    def __init__(self):
        self._timestamp = 0.0

    def tick(self, seconds):
        self._timestamp += seconds

    def time(self):
        return self._timestamp


@pytest.fixture
def fakeTimer():
    return FakeTimer()


def test_constructor():
    max_amount = 10
    refill_time = 60
    refill_amount = 10
    timer = time
    bucket = Bucket(max_amount, refill_time, refill_amount, timer)

    assert isinstance(bucket, Bucket)
    assert bucket.get_max_amount() == max_amount
    assert bucket.get_refill_time() == refill_time
    assert bucket.get_refill_amount() == refill_amount
    assert bucket.get_timer().__name__ == time.__name__


def test_get(fakeTimer):
    max_amount = 10
    refill_time = 60
    refill_amount = 5
    # At the start of the timer, should have all tokens
    bucket = Bucket(max_amount, refill_time, refill_amount, fakeTimer)
    assert bucket.get_tokens() == max_amount

    # Fake that 80 seconds passed
    t = bucket.get_timer()
    t.tick(80)
    # Should have all the tokens since no token has been reduced from the bucket
    assert bucket.get_tokens() == max_amount


def test__refill_counter():
    pass


def test_reset():
    pass


def test_reduce_with_refill_time_not_reached(fakeTimer):
    max_amount = 10
    refill_time = 60
    refill_amount = 5

    # At the start of the timer, we should have all the tokens.
    bucket = Bucket(max_amount, refill_time, refill_amount, fakeTimer)
    assert bucket.get_tokens() == max_amount

    # Reduce all tokens
    bucket.reduce(max_amount)

    # Fake that half of the refill time has passed
    t = bucket.get_timer()
    t.tick(refill_time // 2)

    # Should not be any token available since we reduced all the tokens since the refill time has not been reached yet.
    assert bucket.get_tokens() == 0


def test_reduce_with_refill_time_reached(fakeTimer):
    max_amount = 10
    refill_time = 60
    refill_amount = 5

    # At the start of the timer, we should have all the tokens.
    bucket = Bucket(max_amount, refill_time, refill_amount, fakeTimer)
    assert bucket.get_tokens() == max_amount

    # Reduce all tokens
    bucket.reduce(max_amount)

    # Fake that the refill time has been reached.
    t = bucket.get_timer()
    t.tick(refill_time + 1)

    # Should have 5 tokens available since the refill time has been reached
    assert bucket.get_tokens() == refill_amount


def test_reduce_with_multiple_refill_time_reached(fakeTimer):
    max_amount = 10
    refill_time = 60
    refill_amount = 5

    # At the start of the timer, we should have all the tokens.
    bucket = Bucket(max_amount, refill_time, refill_amount, fakeTimer)
    assert bucket.get_tokens() == max_amount

    # Reduce all tokens
    bucket.reduce(max_amount)

    # Fake that the refill time has been reached 3 times.
    t = bucket.get_timer()
    t.tick(refill_time * 3 + 1)

    # Should be the max_amount(10) since we did not reduce any token.
    assert bucket.get_tokens() == max_amount
    assert bucket.get_tokens() != refill_time * 3
