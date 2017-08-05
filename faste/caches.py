"""
Copyright (c) 2017 Patrick Dill, a/k/a reshanie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import collections

from .util import hashable
from random import choice as random_choice


# ORDER BASED CACHES


class RRCache(object):
    """
    Random Replacement cache.

    When the cache reaches max_size, keys will randomly be evicted to make room.

    Parameters
    ----------
    max_size : int
        Max size of the cache. Must be > 0
    populate : dict
        Keyword argument with values to populate cache with, in no given order. Can't be larger than max_size
    """

    def __init__(self, max_size, populate=None):
        self.max_size = max(max_size, 1)
        self._store = collections.OrderedDict()

        if populate:
            if len(populate) > self.max_size:
                raise ValueError("dict too large to populate cache with (max_size={0!r})".format(self.max_size))

            self.update(**populate)

    def __setitem__(self, key, value):
        if not hashable(key):
            raise TypeError("unhashable type: {0!r}".format(type(key.__class__.__name__)))

        if len(self._store)+1 > self.max_size:
            to_evict = random_choice(self.keys())

            del self[to_evict]
        self._store[key] = value

        return value

    def __getitem__(self, item):
        if item not in self._store:
            raise KeyError("key {0!r} not in cache".format(item))

        return self._store[item]

    def __delitem__(self, key):
        self.pop(key)

    def __iter__(self):
        return iter(self.keys())

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, repr([(k, v) for k, v in self._store.items()]))

    def __len__(self):
        return len(self._store)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.items() == other.items()

    def __contains__(self, item):
        return item in self.keys()

    def update(self, *args, **kwargs):
        for kv in args:
            self[kv[0]] = kv[1]

        for k, v in kwargs.items():
            self[k] = v

    def get(self, key, default=None):
        if key not in self.keys():
            return default

        return self[key]

    @property
    def size(self):
        """
        Size of cache (# of keys stored

        :returns: int
        """
        return len(self._store)

    def pop(self, key, default=None):
        """
        Pops key from cache, if it exists. Else returns default

        :param key: key to pop
        :keyword default: Default value if key doesn't exist

        :returns: value of popped item or default
        """
        return self._store.pop(key, default)

    def popitem(self, last=False):
        """
        Pops item from cache.

        :keyword last: If True, pops least recently used item, else, pops most recently used

        :returns: Tuple value of popped item (key, value) or None if there was nothing to pop
        """
        return self._store.popitem(last=last)

    def move_to_end(self, key, last=True):
        """
        Moves key in cache to either end.

        :param key: Key to move
        :keyword last: If True, moves to right end, if False, moves to beginning.
        """
        return self._store.move_to_end(key, last=last)

    def items(self):
        return list(self._store.items())

    def keys(self):
        return list(self._store.keys())

    def values(self):
        return list(self._store.values())


class FIFOCache(RRCache):
    """
    First In First Out cache.

    When the max_size is reached, the cache evicts the last key set without any regard to how often or how many times it
    was accessed before.

    Parameters
    ----------
    max_size : int
        Max size of the cache. Must be > 0
    populate : dict
        Keyword argument with values to populate cache with, in no given order. Can't be larger than max_size
    """
    def __init__(self, max_size, populate=None):
        super().__init__(max_size, populate=populate)

    def __setitem__(self, key, value):
        if not hashable(key):
            raise TypeError("unhashable type: {0!r}".format(type(key.__class__.__name__)))

        self._store[key] = value
        if len(self._store) > self.max_size:
            self._store.popitem(last=False)
        return value


class LRUCache(FIFOCache):
    """
    Least recently used cache implementation.

    When the max size is reached, the least recently used value is evicted from the cache.

    Parameters
    ----------
    max_size : int
        Max size of the cache. Must be > 0
    populate : dict
        Keyword argument with values to populate cache with, in no given order. Can't be larger than max_size
    """

    def __init__(self, max_size, populate=None):
        super().__init__(max_size, populate=populate)

    def __getitem__(self, item):
        if item not in self._store:
            raise KeyError("key {0!r} not in cache".format(item))

        self._store.move_to_end(item)
        return self._store[item]


class MRUCache(FIFOCache):
    """
    Most recently used cache implementation.

    When the max size is reached, the most recently used value is evicted from the cache. This is useful in applications
    where older keys are more likely to be accessed.

    Parameters
    ----------
    max_size : int
        Max size of the cache. Must be > 0
    populate : dict
        Keyword argument with values to populate cache with, in no given order. Can't be larger than max_size
    """

    def __init__(self, max_size, populate=None):
        super().__init__(max_size, populate=populate)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

        self._store.move_to_end(key, last=False)
        return value

    def __getitem__(self, item):
        if item not in self._store:
            raise KeyError("key {0!r} not in cache".format(item))

        self._store.move_to_end(item, last=False)
        return self._store[item]


# FREQUENCY BASED CACHES


class LFUCache(object):
    """
    Least Frequently Used cache.

    When max_size is reached, the least frequently accessed item is evicted from the cache.

    Parameters
    ----------
    max_size : int
        Maximum # of items that can exist in the cache
    populate : dict
        Values to pre-populate the cache with, in no given order.
    """
    def __init__(self, max_size, populate=None):
        self.max_size = max(max_size, 1)

        self._store = {}  # example store values: {key: [value, access_frequency]}

        if populate:
            if len(populate) > self.max_size:
                raise ValueError("dict too large to populate cache with (max_size={0!r})".format(self.max_size))

            self.update(**populate)

    def __delitem__(self, key):
        del self._store[key]

    def __setitem__(self, key, value):
        if len(self._store)+1 > self.max_size:
            del self._store[self.least_frequent()[0]]

        self._store[key] = [value, 0]  # {key: [value, access_frequency]}

    def __getitem__(self, key):
        if key not in self._store:
            raise KeyError("key {0!r} doesn't exist in cache".format(key))

        self._store[key][1] += 1
        return self._store[key][0]

    def __iter__(self):
        return iter(self.keys())

    def __repr__(self):
        ordered = sorted(self._store.items(), key=lambda x: -x[1][1])

        return "{}({})".format(self.__class__.__name__, repr([(k, v[0]) for (k, v) in ordered]))

    def __len__(self):
        return len(self._store)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.items() == other.items()

    def __contains__(self, item):
        return item in self.keys()

    def pop(self, key):
        """
        Pops key from cache

        :param key: Key to pop
        :returns: Key's value in cache
        """
        if key not in self._store.keys():
            raise KeyError("key {0!r} doesn't exist in cache".format(key))

        v = self._store[key][0]
        del self[key]

        return v

    def popitem(self):
        """
        Removes least frequent item in cache and returns key, value pair

        :returns: tuple
        """
        lf = self.least_frequent()
        if lf:
            del self[lf[0]]
            return lf

    def keys(self):
        return self._store.keys()

    def values(self):
        return [v[0] for v in self._store.values()]

    def items(self):
        return [(k, self._store[k][0]) for k in self._store.keys()]

    def least_frequent(self):
        """
        Gets key, value pair for least frequent item in cache

        :returns: tuple
        """
        if len(self._store) == 0:
            return

        kv = min(self._store.items(), key=lambda x: x[1][1])

        return kv[0], kv[1][0]

    def update(self, *args, **kwargs):
        for kv in args:
            self[kv[0]] = kv[1]

        for k, v in kwargs.items():
            self[k] = v

    def get(self, key, default=None):
        if key not in self.keys():
            return default

        return self[key]

    @property
    def size(self):
        return len(self._store)
