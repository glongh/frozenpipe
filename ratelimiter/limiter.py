from ratelimiter import Bucket


class Limiter:
    def __init__(self, buckets: [Bucket]) -> None:
        self.__buckets = buckets
        self.__depleted = set()

    def reduce(self, tokens=1) -> bool:
        """
        Returns a boolean value indicating if the tokens requested can be used and
        removes them from the all the buckets.
        """

        # Look for buckets with no tokens left and update the depleted list
        self.__depleted = set(
            [key for key, bucket in enumerate(self.__buckets) if bucket.get_tokens() < tokens])

        # Check if one or more limits has been reached. If so, return false.
        if len(self.__depleted) > 0:
            return False

        # Reduce tokens for all the buckets in the limiter
        for bucket in self.__buckets:
            bucket.reduce(tokens)

        return True

    def get_bucket_status(self, key) -> int:
        """
        Return the number of tokens remaining in the requested bucket
        """
        return self.__buckets[key].get_tokens()

    def get_buckets_status(self) -> dict:
        """
        Returns the status of all buckets in a dictionary form
            key: Index in the bucket list
            value: The remaining tokens in the bucket
        """
        return {key: bucket.get_tokens() for key, bucket in enumerate(self.__buckets)}

    def get_bucket_depleted(self) -> set:
        """
        Returns a list of indices of the buckets without tokens
        """
        return self.__depleted

    def get_buckets(self):
        return self.__buckets
