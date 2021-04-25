from ratelimiter import Limiter, Bucket, Time as per
from test_tools import FakeTimer
import time
import pytest


def test_constructor():
    buckets = [
        Bucket(max_amount=10, refill_amount=1,
               refill_time=per.MINUTE, timer=time),
        Bucket(max_amount=5, refill_amount=5,
               refill_time=per.MINUTE, timer=time)
    ]
    rate_limiter = Limiter(buckets)
    assert isinstance(rate_limiter, Limiter)
    empty_set = set()
    assert rate_limiter.get_bucket_depleted() == empty_set
    assert len(rate_limiter.get_buckets()) == len(buckets)


def test_get_buckets_status():
    buckets = [
        Bucket(max_amount=10, refill_amount=1,
               refill_time=per.MINUTE, timer=time),
        Bucket(max_amount=5, refill_amount=5,
               refill_time=per.MINUTE, timer=time)
    ]
    rate_limiter = Limiter(buckets)

    assert rate_limiter.get_buckets_status()[0] == buckets[0].get_tokens()
    assert rate_limiter.get_buckets_status()[1] == buckets[1].get_tokens()


def test_get_bucket_status():
    buckets = [
        Bucket(max_amount=10, refill_amount=1,
               refill_time=per.MINUTE, timer=time),
        Bucket(max_amount=5, refill_amount=5,
               refill_time=per.MINUTE, timer=time)
    ]
    rate_limiter = Limiter(buckets)
    assert rate_limiter.get_bucket_status(0) == buckets[0].get_tokens()


def test_get_bucket_status_with_no_tokens_one_bucket():
    fakeTimer = FakeTimer()
    buckets = [
        Bucket(max_amount=10, refill_amount=1,
               refill_time=per.MINUTE, timer=fakeTimer)
    ]
    rate_limiter = Limiter(buckets)
    # Reduce all the tokens
    assert rate_limiter.reduce(10) == True

    # Reduce one token over
    assert rate_limiter.reduce(1) == False


def test_get_bucket_status_with_no_tokens_one_bucket():
    fakeTimer = FakeTimer()
    buckets = [
        Bucket(max_amount=10, refill_amount=1,
               refill_time=per.MINUTE, timer=fakeTimer)
    ]
    rate_limiter = Limiter(buckets)
    assert rate_limiter.reduce(5) == True
    assert rate_limiter.reduce(5) == True


def test_get_bucket_status_with_refill():
    fakeTimer = FakeTimer()
    buckets = [
        Bucket(max_amount=10, refill_amount=1,
               refill_time=per.MINUTE, timer=fakeTimer)
    ]
    rate_limiter = Limiter(buckets)
    assert rate_limiter.reduce(5) == True
    assert rate_limiter.reduce(5) == True

    buckets = rate_limiter.get_buckets()
    t = buckets[0].get_timer()
    t.tick(per.MINUTE + 1)

    assert rate_limiter.reduce(1) == True


def test_get_bucket_status_with_refill_not_reached():
    fakeTimer = FakeTimer()
    buckets = [
        Bucket(max_amount=10, refill_amount=1,
               refill_time=per.MINUTE, timer=fakeTimer)
    ]
    rate_limiter = Limiter(buckets)
    assert rate_limiter.reduce(5) == True
    assert rate_limiter.reduce(5) == True

    buckets = rate_limiter.get_buckets()
    t = buckets[0].get_timer()
    t.tick(per.MINUTE // 2)

    assert rate_limiter.reduce(1) == False
