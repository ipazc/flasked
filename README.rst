=============
Flasked 0.0.4
=============

`Flasked` is a package designed to ease the creation of a REST API. It uses `Flask` and `Flask-Restful` in the
background.

.. image:: https://badge.fury.io/py/flasked.svg
    :target: https://badge.fury.io/py/flasked


Example
=======

How to create a RESTFUL API faster than this?

.. code:: python

    from flasked import Flasked

    class Root():
        def get(self):
            return "This is the result"

    flasked = Flasked()
    flasked["/"] = Root
    flasked.run()


Installation
============

It is only supported **Python 3.4.1** onwards:

.. code:: bash

    sudo pip3 install flasked


Description
===========

`Flasked` behaves like a Python's dict; thus, in order to create more entry points, it is only required to assign the
route with the class that manages the route. Example:

.. code:: python

    flasked["/"] = RouteRoot
    flasked["/route2/"] = Route2
    flasked["/route2/<variable>/"] = Route3


The routes available can be iterated in the same way as a Python's dict:

.. code:: python
    
    print(list(flasked.keys()))
    
    for route in flasked:
        print(route)
    
    for route, cls in flasked.items():
        print("{}: {}".format(route, cls))


The classes that manages the routes *do not require* to inherit from any special class, since `Flasked` is able to manage them.
Nonetheless, they have access to all the methods and attributes that a `Resource <https://github.com/flask-restful/flask-restful/blob/master/flask_restful/__init__.py#L564>`_ class has (from `Flask_Restful <https://github.com/flask-restful/>`_).


The HTTP methods are defined as method from the class that handles it:

.. code:: python

    class Root():
        def get(self):
            return {"result": "result for GET"}

        def post(self):
            return {"result": "result for POST"}

        def delete(self):
            return {"result": "result for DELETE"}


Also, when a variable is defined in an entry URL, the class method's need to reflect it:

.. code:: python

    class Route3():
        def get(self, variable):
            return variable

    flasked["/route2/<variable>/"] = Route3


In order to run flask, it is only required to execute the `run()` method. It has the same arguments as a `Flask app run()`:

.. code:: python

    flasked.run(host="0.0.0.0", port=2234, threaded=True, debug=False)


The flask_restful API object and the Flask original APP object are directly accessible from the `flasked` object

.. code:: python

    # Flask_Restful API object
    api = flasked.api

    # Flask API object
    flask_app = flasked.flask_app


ADVANCED
========

If the class that manages a route requires arguments to be injected in the constructor, it can be done in the following way:

.. code:: python

    class Route():
        def __init__(self, argument1, argument2):
            self.argument1 = argument1
            self.argument2 = argument2

        def get(self, variable):
            return variable

    # The following 3 lines do the same:
    flasked["/"] = Route, argument1, argument2                                          # First way
    flasked["/"] = Route, {'args': [argument1, argument2]}                              # Second way
    flasked["/"] = Route, {'kwargs': dict(argument1=argument1, argument2=argument2)}    # third way


**IMPORTANT:** Note that if the first way is taken, the `argument1` **can't be a dictionary that contains the keywords 'args' or 'kwargs'**.
Otherwise, it will be used as a source for the `args` and `kwargs` of the initializer. It is always preferred to use the second mixed with the third way.

This package is completely compatible with flask_restful. For more information, check `Flask_Restful <https://github.com/flask-restful/>`_.


BASIC USE CASES
===============

Basic usage examples are shown in the `Usage-examples page from the wiki <https://github.com/ipazc/flasked/wiki/Usage-examples>`_:

 * `How to create endpoints with different methods <https://github.com/ipazc/flasked/wiki/Usage-examples#create-get-post-delete--endpoints>`_
 * `How to read a json from the request <https://github.com/ipazc/flasked/wiki/Usage-examples#retrieve-a-json-from-request>`_
 * `How to read a request parameter <https://github.com/ipazc/flasked/wiki/Usage-examples#retrieve-a-raw-parameter-from-request>`_
 * `How to read a request URL value <https://github.com/ipazc/flasked/wiki/Usage-examples#retrieve-a-value-from-url-path>`_
 * `How to retrieve a file from the request <https://github.com/ipazc/flasked/wiki/Usage-examples#retrieve-a-binary-file-from-request>`_
 * `How to return a file as response <https://github.com/ipazc/flasked/wiki/Usage-examples#return-a-binary-file-as-response-to-request>`_


MANUAL TESTING
==============

If you want to test your API REST manually, there's an explanation on how to do it in this `wiki page <https://github.com/ipazc/flasked/wiki/Manual-testing>`_

LICENSE
=======

It is released under the *MIT license*.