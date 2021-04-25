from http.server import BaseHTTPRequestHandler, HTTPServer
from ratelimiter import Limiter, Bucket, Time as per
import time
import socketserver
import json

PORT = 8080
HOST = '127.0.0.1'

buckets = [
    Bucket(
        # Rate of 1 per 1 second
        refill_amount=1, refill_time=per.SECOND - 0.1,
        max_amount=10, timer=time
    ), Bucket(
        # Rate of 5 per 5 seconds
        refill_amount=5, refill_time=(per.SECOND - 0.1) * 5,
        max_amount=5, timer=time
    ), Bucket(
        # Rate of 10 per 10 seconds
        refill_amount=10, refill_time=(per.SECOND - 0.1) * 10,
        max_amount=10, timer=time
    )
]
rate_limiter = Limiter(buckets)


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            bucket_status = rate_limiter.get_buckets_status()
            print({"Bucket {}".format(key): bucket_status[key] for key in bucket_status})

        if rate_limiter.reduce():
            self.send_response(200)
        else:
            self.send_response(403)
        self.end_headers()


if __name__ == "__main__":
    webServer = HTTPServer((HOST, PORT), ServerHandler)
    print("Server started http://%s:%s" % (HOST, PORT))

    webServer.serve_forever()
