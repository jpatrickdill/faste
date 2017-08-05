dictionary style caches
=======================

Faste is a cache library to allow many different cache algorithms in Python, with the functionality of a regular dict.
Anything you can do to a dict, you can do to these caches.

All The Caches(tm) ::

    import faste

    # Random Replacement
    # When cache is full, random items are removed to make space for new ones
    RR = faste.RRCache(max_items)

    # First In First Out
    # When cache is full, cache evicts the last key that was set
    FIFO = faste.FIFOCache(max_items)

    # Least Recently Used
    # When cache is full, least recently accessed item is evicted
    LRU = faste.LRUCache(max_items)

    # Most Recently Used
    # When cache is full, most recently accessed item is evicted
    # Useful for caches where old data is more commonly accessed
    MRU = faste.MRUCache(max_items)

    # Least Frequently Used
    # When cache is full, least frequently accessed item is evicted
    LFU = faste.LFUCache(max_items)

