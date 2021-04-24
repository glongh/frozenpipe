from ratelimiter.bucket import Bucket
import time


def test_constructor():
    max_amount = 10
    refill_time = 60
    refill_amount = 10
    timer = time
    bucket = Bucket(max_amount, refill_time, timer)

    assert isinstance(bucket, Bucket)
    assert bucket.get_max_amount() == max_amount
    assert bucket.get_refill_time() == refill_time
    assert bucket.get_refill_amount() == refill_amount
    assert bucket.get_timer().__name__ == time.__name__
