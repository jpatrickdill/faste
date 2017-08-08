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

from .util import hashable
from . import caches


class CachedFunc:
    def __init__(self, cache, func, *args, **kwargs):
        self.func = func
        self.cache = cache(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        call_with = tuple(list(args)+list(kwargs.items()))

        if not hashable(call_with):
            raise TypeError("Unhashable args+kwargs given: {0!r} {1!r}".format(args, kwargs))

        if call_with not in self.cache:
            self.cache[call_with] = self.func(*args, **kwargs)

        return self.cache[call_with]

    def clear_cache(self):
        self.cache.clear()


def timed_cache(timeout, max_size=128):
    """
    Timed cache decorator

    :param int timeout: cache timeout
    :param int max_size: max cache size
    """

    def new_decorator(func):
        wrapped = CachedFunc(caches.TimeoutCache, func, timeout, max_size=max_size)
        wrapped.__name__ = func.__name__
        wrapped.__doc__ = func.__doc__
        wrapped.__module__ = func.__module__
        return wrapped
    return new_decorator


def rr_cache(max_size=128):
    """
    Random Replacement cache decorator

    :param int max_size: max cache size
    """

    def new_decorator(func):
        wrapped = CachedFunc(caches.RRCache, func, max_size)
        wrapped.__name__ = func.__name__
        wrapped.__doc__ = func.__doc__
        wrapped.__module__ = func.__module__
        return wrapped
    return new_decorator


def lfu_cache(max_size=128):
    """
    Least Frequently Used cache decorator

    :param int max_size: max cache size
    """

    def new_decorator(func):
        wrapped = CachedFunc(caches.LFUCache, func, max_size)
        wrapped.__name__ = func.__name__
        wrapped.__doc__ = func.__doc__
        wrapped.__module__ = func.__module__
        return wrapped
    return new_decorator
