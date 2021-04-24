from ratelimiter.time import Time


def test_time():
    assert Time.SECOND == 1
    assert Time.MINUTE == 60
    assert Time.HOUR == Time.MINUTE * 60


def test_day():
    assert Time.DAY == 24 * Time.HOUR
    assert Time.WEEK == 7 * 24 * Time.HOUR
    assert Time.MONTH == 30 * 24 * Time.HOUR
    assert Time.YEAR == 365 * 24 * Time.HOUR
