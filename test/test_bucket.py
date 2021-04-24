from ratelimiter.bucket import Bucket
import time
import pytest


class FakeTimer():
    '''
    A fake timer to test against time
    '''

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
    refill_amount = 10
    # At the start of the timer, should have all tokens
    bucket = Bucket(max_amount, refill_time, refill_amount, fakeTimer)
    assert bucket.get() == max_amount

    # Fake that 80 seconds passed
    t = bucket.get_timer()
    t.tick(80)
    # Should have all the tokens since no token has been reduced from the bucket
    assert bucket.get() == max_amount
