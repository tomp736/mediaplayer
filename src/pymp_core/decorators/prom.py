from prometheus_client import Counter
prom_counters = {}


def counter_increment(key: str, amount: float = 1):
    key = key.lower()
    key = key.replace('.', '_')
    prom_counter = prom_counters.get(key, None)
    if prom_counter is None:
        prom_counter = Counter(name=key, documentation=key)
        prom_counters[key] = prom_counter
    prom_counter.inc(amount)


def prom_count(func):
    def increment(*args, **kwargs):
        counter_increment(f"{func.__module__}_{func.__name__}")
        return func(*args, **kwargs)
    return increment
