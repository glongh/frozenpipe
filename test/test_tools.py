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
