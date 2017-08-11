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

from . import caches
from .util import hashable

_caches = {}


def _cached_func(func, cache, *a, **kw):
    if id(func) not in _caches:
        _caches[id(func)] = cache(*a, **kw)

    def wrapper(*args, **kwargs):
        call_with = tuple(args + tuple(kwargs.items()))
        if not hashable(call_with):
            raise TypeError("Unhashable args/keywords given for cached function {}".format(func.__name__))

        if call_with not in _caches[id(func)]:
            _caches[id(func)][call_with] = func(*args, **kwargs)

        return _caches[id(func)][call_with]

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__

    def _clear():
        _caches[id(func)].clear()

    wrapper.clear_cache = _clear

    return wrapper


def rr_cache(max_size=128):
    """
    Random Replacement cache decorator

    :keyword int max_size: max cache size
    """

    def actual_decorator(func):
        return _cached_func(func, caches.RRCache, max_size)

    return actual_decorator


def lfu_cache(max_size=128):
    """
    Least Frequently Used cache decorator

    :keyword max_size: max cache size
    """

    def actual_decorator(func):
        return _cached_func(func, caches.LFUCache, max_size)

    return actual_decorator


def timed_cache(timeout, max_size=128):
    """
    Time based decorator

    :param timeout: Cache key timeout
    :keyword max_size: Max size
    """

    def actual_decorator(func):
        return _cached_func(func, caches.TimeoutCache, timeout, max_size=max_size)

    return actual_decorator
