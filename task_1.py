import random
import time
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key) 
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)  
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  

def range_sum_no_cache(array, L, R):
    return sum(array[L-1:R])

def update_no_cache(array, index, value):
    array[index-1] = value

def range_sum_with_cache(array, L, R, cache):
    key = (L, R)
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    result = sum(array[L-1:R])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value, cache):
    array[index-1] = value
    keys_to_remove = [key for key in cache.cache if index >= key[0] and index <= key[1]]
    for key in keys_to_remove:
        del cache.cache[key]

def generate_test_data(n, q):
    array = [random.randint(1, 100) for _ in range(n)]
    queries = []
    for _ in range(q):
        query_type = random.choice(["Range", "Update"])
        if query_type == "Range":
            L = random.randint(1, n)
            R = random.randint(L, n)
            queries.append(('Range', L, R))
        else:
            index = random.randint(1, n)
            value = random.randint(1, 100)
            queries.append(('Update', index, value))
    return array, queries

def measure_time(n, q, cache_size):
    array_no_cache, queries_no_cache = generate_test_data(n, q)
    array_with_cache, queries_with_cache = generate_test_data(n, q)

    start_time = time.time()
    for query in queries_no_cache:
        if query[0] == 'Range':
            range_sum_no_cache(array_no_cache, query[1], query[2])
        else:
            update_no_cache(array_no_cache, query[1], query[2])
    end_time = time.time()
    no_cache_time = end_time - start_time

    cache = LRUCache(cache_size)
    start_time = time.time()
    for query in queries_with_cache:
        if query[0] == 'Range':
            range_sum_with_cache(array_with_cache, query[1], query[2], cache)
        else:
            update_with_cache(array_with_cache, query[1], query[2], cache)
    end_time = time.time()
    cache_time = end_time - start_time

    return no_cache_time, cache_time

if __name__ == '__main__':
    n = 100000  
    q = 50000   
    cache_size = 1000  

    no_cache_time, cache_time = measure_time(n, q, cache_size)

    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")
