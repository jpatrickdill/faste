import timeit

import faste

n = 100000

max_size = 128

print("\nFaste Testing\n"
      "-------------\n")

for cache_ in [faste.caches.RRCache,
               faste.caches.FIFOCache,
               faste.caches.LRUCache,
               faste.caches.MRUCache,
               faste.caches.LFUCache]:

    cache = cache_(max_size)

    s = timeit.timeit("cache['abc'] = 'abcdef'", number=n, globals={"cache": cache}) / n
    g = timeit.timeit("cache['abc']", number=n, globals={"cache": cache}) / n

    print("{0.__name__}".format(cache_))
    print("set value : {:.2}ms".format(s * 1000))
    print("get value : {:.2}ms\n".format(g * 1000))
