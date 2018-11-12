Client API Reference
--------------------

All commands are accessed through the `udfsapi.Client` class.

### Exceptions

```eval_rst
.. automodule:: udfsapi.exceptions
    :members:
```



### The API Client

All methods accept the following parameters in their `kwargs`:

 * **opts** (*dict*) – A dictonary of custom parameters to be sent with the
                       HTTP request

```eval_rst
.. autofunction:: udfsapi.connect

.. autofunction:: udfsapi.assert_version

.. autoclass:: udfsapi.Client
    :members:
    :show-inheritance:

```
