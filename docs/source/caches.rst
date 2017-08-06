
Caches
======

.. toctree::
    :maxdepth: 3
    :caption: Contents:

Faste supports several cache algorithms, each with their own benefits. If you want more information on any of these,
you can find them on Wikipedia. https://en.wikipedia.org/wiki/Cache_replacement_policies

All of these caches support every dictionary method. https://docs.python.org/3/library/stdtypes.html#dict

.. currentmodule:: faste.caches

Random Replacement
------------------

.. autoclass:: RRCache
    :members:

First In First Out
------------------

.. autoclass:: FIFOCache
    :members:

Least Recently Used
-------------------

.. autoclass:: LRUCache
    :members:

Most Recently Used
------------------

.. autoclass:: MRUCache
    :members:

Least Frequently Used
---------------------

.. autoclass:: LFUCache
    :members:

Timeout based cache
-------------------

.. autoclass:: TimeoutCache
    :members:
