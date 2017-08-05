from setuptools import setup, find_packages
import faste

long_desc = """
dictionary style caches
=======================

Faste is a cache library to allow many different cache algorithms in Python, with the functionality of a regular dict.
Anything you can do to a dict, you can do to these caches. https://docs.python.org/3/library/stdtypes.html#dict

All The Caches(tm)
~~~~~~~~~~~~~~~~~~

Every cache has the signature CacheNameHere(max_items)

max_items is the max length of the cache before items start getting evicted.

.. code:: python

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

"""

setup(
    name='faste',
    description="dictionary style caches.",
    long_description=long_desc,
    version=faste.__version__,
    url='https://github.com/reshanie/faste',
    license='MIT',
    author='Patrick Dill, a/k/a reshanie',
    author_email='jamespatrickdill@gmail.com',
    install_requires=[],
    download_url="http://github.com/reshanie/faste/archive/master.tar.gz",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    keywords="cache caches LIFO FIFO RR LRU MRU LFU memory dict dictionary",

    packages=find_packages(exclude=["docs", ".idea"]),
)
