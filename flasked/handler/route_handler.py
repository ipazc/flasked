#
# MIT License
#
# Copyright (c) 2017-2024 Iván de Paz Centeno
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



class RouteHandler:
    """
    Manages route handlers, including initialization with arguments and keyword arguments,
    and checks for method availability on the handler.
    """
    def __init__(self, prototype, init_args=None, init_kwargs=None):
        """
        Initializes a new RouteHandler instance.
        :param prototype: The handler class to be instantiated for a route.
        :param init_args: Optional tuple of arguments for the handler class instantiation.
        :param init_kwargs: Optional dictionary of keyword arguments for the handler class instantiation.
        """
        init_args = init_args or tuple()
        init_kwargs = init_kwargs or dict()
        
        self._prototype = prototype
        self._init_args = init_args
        self._init_kwargs = init_kwargs

    def hasmethod(self, m):
        """
        Checks if the prototype has a method corresponding to an HTTP method.
        :param m: HTTP method to check.
        :return: True if the method exists, False otherwise.
        """
        return hasattr(self._prototype, m.lower())

    @property
    def name(self):
        """
        Returns the name of the prototype class.
        """
        return getattr(self._prototype, "name", self._prototype.__name__)
    
    @property
    def description(self):
        """
        Attempts to return the 'description' attribute of the prototype. Returns an empty string if not found.
        """
        return getattr(self._prototype, "description", self._prototype.__doc__)
    
    def __call__(self):
        """
        Instantiates the prototype with the provided arguments and keyword arguments.
        """
        return self._prototype(*self._init_args, **self._init_kwargs)
