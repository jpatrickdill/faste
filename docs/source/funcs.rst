Function Memoizing
==================

Caches can also be used to store function calls, as a way of memoize.

Because this is dict based, any function calls must have hashable
arguments & keywords. Better to not cache than to blow up entirely.

Example ::

    import faste

    @faste.decor.timed_cache(120, max_size=10)
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

Note: These don't store information on the parenting object of the function, so they may not work
correctly with methods.

.. currentmodule:: faste.decor

.. autofunction:: timed_cache

.. autofunction:: rr_cache

.. autofunction:: lfu_cache
