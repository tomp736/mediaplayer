from prometheus_client import Counter


class Prometheus(object):
    counters = {}

    def count(self, key: str, amount: float = 0):
        counter = self.counters.get(key, None)
        if counter is None:
            counter = Counter(name=key, documentation=key)
            self.counters[key] = counter

        counter.inc(amount)


prometheus = Prometheus()
