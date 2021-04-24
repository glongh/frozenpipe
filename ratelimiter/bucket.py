import time


class Bucket:
    def __init__(self, max_amount: int, refill_time: int, refill_amount: int, timer: time) -> None:
        self.__max_amount = max_amount
        self.__refill_time = refill_time
        self.__refill_amount = refill_amount
        self.__timer = timer
        self.__value = max_amount
        self.__ts_updated = timer.time()

    def get_max_amount(self) -> int:
        return self.__max_amount

    def get_refill_time(self) -> int:
        return self.__refill_time

    def get_refill_amount(self) -> int:
        return self.__refill_amount

    def get_timer(self) -> int:
        return self.__timer

    def __refill_counter(self) -> int:
        if self.__refill_time <= 0:
            return 0
        else:
            now = self.__timer.time()
            return int(((now - self.__ts_updated) / self.__refill_time))

    def get_tokens(self) -> int:
        """
        Returns the quantity of available tokens
        """
        tokens = min(self.__max_amount, self.__refill_counter() *
                     self.__refill_amount + self.__value)
        return tokens

    def reset(self) -> None:
        self.__value = self.__max_amount
        self.__ts_updated = self.__timer.time()

    def reduce(self, tokens_to_use: int) -> bool:
        """
        Returns a boolean value indicating if the tokens requested can be used and
        removes them from the bucket.
        """

        refill_count = self.__refill_counter()
        self.__value += refill_count * self.__refill_amount
        self.__ts_updated += refill_count * self.__refill_time

        # Check If the values refilled exceed the maximun allowed. If so, reset to initial state.
        if self.__value >= self.__max_amount:
            self.reset()

        # Check if the tokens requested are more thant the amount available in the bucket
        if tokens_to_use > self.__value:
            return False
        else:
            # Otherwise, update the bucket value and return true
            self.__value -= tokens_to_use
            return True
