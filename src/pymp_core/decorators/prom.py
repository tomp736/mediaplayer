import time
from prometheus_client import Counter
prom_counters = {}


def counter_increment(key: str, amount: float = 1):
    key = key.lower()
    key = key.replace('.', '_')
    counter = prom_counters.get(key, None)
    if counter is None:
        counter = Counter(name=key, documentation=key)
        prom_counters[key] = counter
    counter.inc(amount)


def prom_count_method_call(func):
    def increment(*args, **kwargs):
        counter_increment(f"{func.__module__}_{func.__name__}")
        return func(*args, **kwargs)
    return increment


def prom_count_method_time(func):
    def increment(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        counter_increment(
            f"{func.__module__}_{func.__name__}_seconds", time_end - time_start)
        return result
    return increment
