Function Memoizing
==================

Caches can also be used to store function calls, as a way of memoize.

Because this is dict based, any function calls must have hashable
arguments & keywords. Better to not cache than to blow up entirely.

Example ::

    import faste

    @faste.decor.rr_cache()
    def takes_long(*args):
        time.sleep(5)
        return args

    takes_long()
    # waits 5 seconds before returning ()

    takes_long()
    # returns () immediately

    takes_long("a", "b", "c")
    # waits 5 seconds before returning ("a", "b", "c",)

    takes_long("a", "b", "c")
    # returns ("a", "b", "c",) immediately


Cache Decorators
----------------

.. currentmodule:: faste.decor

.. autofunction:: timed_cache

.. autofunction:: rr_cache

.. autofunction:: lfu_cache
