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

    def get(self):
        '''
        Returns the quantity of available tokens
        '''
        print(self.__max_amount, self.__refill_counter(),
              self.__refill_amount)
        tokens = min(self.__max_amount, self.__refill_counter() +
                     self.__refill_amount)

        return tokens
