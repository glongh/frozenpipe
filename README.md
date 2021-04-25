# Frozen Pipe :stopwatch: :wastebasket: :snowflake:

> Important: This is a python 3 module

A python3 implementation of a general purpose rate limiter

## What’s a rate limiter?

At a high level, a rate limiter limits the number of events an entity can perform in a certain time period.

For example:

- “A single IP can only create 20 accounts per day”.
- “Devices are allowed 5 failed credit card transactions per day”.
- “Users may only send 1 message per day with risky keywords”.

The standard algorithm for rate limiting is called a token bucket, sometimes called a “leaky bucket”. Each bucket has a key index and initially contains the maximum number of tokens. Every time an event occurs, we check if the bucket contains enough tokens and reduce the number of tokens in the bucket by the requested amount. After a period of time called the refill time, the number of tokens in the bucket is increased by the refill amount. Over time, these refills will fill up the bucket to the maximum number of tokens.

Token buckets with customizable refill amounts let you express more complex rate limits like:

- “Each user account is allowed a maximum of 10 failed logins per hour, which refill at a rate of 1 login per hour”.
- “Each geocoded shipping address is allowed a maximum of $200 worth of purchases per day from a risky country email addresses, which refills at a rate of $50 per day”.

As you can see, these rate limits allow a lot of freedom for legitimate user behavior, but quickly clamp down on repeated violations.

## Quick start

Import the module and initializes the rate limiter with the buckets.

```python
from ratelimiter import Limiter, Bucket, Time as per

# Initialize the bucket or buckets with the rules
buckets = [
    Bucket(
        # Rate of 1 per 1 second
        refill_amount=1, refill_time=per.SECOND,
        max_amount=10, timer=time
    )
    , Bucket(
        # Rate of 5 per 5 minutes
        refill_amount=5, refill_time=per.MINUTE,
        max_amount=5, timer=time
    )
    , Bucket(
        # Rate of 1000 per day
        refill_amount=1000, refill_time=per.DAY,
        max_amount=1000, timer=time
    )
]
rate_limiter = Limiter(buckets)

# Use the rate limiter.
if rate_limiter.reduce():
  print("You still have quota.")
else:
  print("You quota is exhausted")

# Display status of the buckets.
print rate_limiter.get_buckets_status()
```

## Testing on a fake server (included)

If you use any virtual env, activate it .

```bash
# Create virtual env (optional)
python -m venv env
# Activate virtual env (optional)
source env/bin/activate
```

and install the dependencies

```bash
(env) python -m pip install -r requirements.txt
```

### Start the server

```bash
# Start the test server
(env) python server.py
```

```bash
# Send a single HTTP GET request with curl
curl http://127.0.0.1:8080/

# Use a benchmarking tool like 'hey'. One request per second for a total of 100 request.
hey -n 100 -c 1 -q 1 http://127.0.0.1:8080/

# Display the bucket status on the server
# i.e: {'Bucket 0': 8, 'Bucket 1': 4, 'Bucket 2': 2}
hey -n 100 -c 1 -q 1 http://127.0.0.1:8080/status

```

## Unit test the module with pytest

```bash
# Run the unit test
(env) python -m pytest -v

# Run the Unit Test with test coverage
(env) python -m pytest -v --cov=ratelimiter
```

### Cited Work

- https://en.wikipedia.org/wiki/Leaky_bucket
- https://medium.com/smyte/rate-limiter-df3408325846
