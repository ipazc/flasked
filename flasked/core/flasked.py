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

from flask import Flask, request
from werkzeug.serving import BaseWSGIServer

import threading
import warnings
import gc

from flasked.utils.helpers import is_interactive
from flasked.warnings import InteractivePythonWarning
from flasked.handler import RouteHandler
from flasked.iterator import EndpointMatcherIterator


class Flasked:
    """
    Core class of the Flasked framework, managing route definitions, server start/stop,
    and request handling within a Flask application context.

    The class behaves like a Python dictionary. New routes can be dynamically added, changed or removed just modifying
    the key entries in the class.

    Use the .summary property to display the routes in a pretty-printed format.
    """
    def __init__(self, accepted_methods=None, name=__name__):
        """
        Initializes a new Flasked instance with optional HTTP methods and a name for the Flask application.
        :param accepted_methods: Optional list of HTTP methods the server will accept.
        :param name: Optional name for the Flask application.
        """
        self._accepted_methods = accepted_methods or ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
        self._routes = {}
        self._server_thread = None
        self._address = None
        self._port = None
        self._name = name
        self._flask_app = None
        self._build_flask_app()

    def _build_flask_app(self):
        self._flask_app = Flask(self.name)
        self._flask_app.add_url_rule('/', view_func=self._handle_request, defaults={'path': ''}, methods=self._accepted_methods)
        self._flask_app.add_url_rule('/<path:path>', view_func=self._handle_request, methods=self._accepted_methods)

    @property
    def flask_app(self):
        """
        Access to the flask app object. This is useful to change internal flask properties or to pass to a WSGI once
        the routes are configured.
        """
        return self._flask_app

    @property
    def routes(self):
        """
        Wrapper of self. Flasked object is already a dictionary for routes.
        Using this property may make it more readable under certain contexts.
        """
        return self
    
    @property
    def name(self):
        return self._name
    
    @property
    def running(self):
        return self._port is not None

    @property
    def address(self):
        return self._address

    @property
    def port(self):
        return self._port
    
    def items(self):
        return self._routes.items()

    def keys(self):
        return self._routes.keys()

    def values(self):
        return self._routes.values()

    def __contains__(self, item):
        return item in self.routes

    def _add_route(self, endpoint, handler):
        self._routes[endpoint] = handler
        self._routes = dict(sorted(self._routes.items(), key=lambda x: len(x[0]), reverse=True))
        
    def _del_route(self, endpoint):
        del self._routes[endpoint]

    def resolve_endpoint(self, path):
        routes = self._routes
            
        for endpoint in routes:
            match = True
            arguments = {}
            
            try:
                emi = EndpointMatcherIterator(endpoint, path)
    
                # Now we iterate over the iterator
                for matches, ep_segment, argument_name, argument_result in emi:
                    match &= matches
    
                    if argument_name is not None:
                        arguments[argument_name] = argument_result
                        
            except (KeyError, ValueError) as e:
                match = False
    
            if match:
                return endpoint, arguments

        raise KeyError("Endpoint not found")
                
    def _handle_request(self, path, method=None):
        method = method or request.method.lower()
        path = f"/{path}" if not path.startswith("/") else path

        try:
            endpoint, arguments = self.resolve_endpoint(path)
            handler = self._routes[endpoint]()

            view_func = getattr(handler, method)
            response = view_func(**arguments)
        
        except (KeyError, TypeError) as e:
            response = {"error": "Resource not found"}, 404
            
        except AttributeError as e:
            response = {"error": "Method not allowed"}, 405

        return response

    def __getitem__(self, key):
        return self._routes[key]
    
    def __setitem__(self, key, value):
        if not isinstance(value, RouteHandler):
            
            if isinstance(value, tuple):
                cls, args, kwargs = value[0], value[1:], {}
                
                if isinstance(value[-1], dict):
                    kwargs, args = args[-1], args[:-1]

            else:
                cls, args, kwargs = value, None, None
            
            value = RouteHandler(cls, init_args=args, init_kwargs=kwargs)
        
        self._add_route(key, value)

    def __delitem__(self, key):
        self._del_route(key)

    def __len__(self):
        return len(self._routes)

    def __str__(self):
        status_text = {True: f'Running on {self.address}:{self.port}', False: 'Not running'}[self.running]
        return f"[Flasked {self.name} app: {status_text}; {len(self)} routes defined]"
        
    def __repr__(self):
        return str(self)

    @property
    def summary(self):
        routes_str = "\n\t".join([f"{k} ({', '.join([m for m in self._accepted_methods if v.hasmethod(m)])}) - {v.name}: {v.description}" 
                                  for k, v in self._routes.items()])
        summary = f"{str(self)}\n\t{routes_str}"
        print(summary)

    def run(self, host="127.0.0.1", port=1024, threaded=True, debug=False, hijack_port=True, **kwargs):
        if host == "localhost":
            host = "127.0.0.1"
            
        if hijack_port:
            self._address = host
            self._port = port
            self.stop(force=True)
            
        self._address = host
        self._port = port

        if is_interactive() and 'use_reloader' not in kwargs:
            warnings.warn("Running inside an interactive environment. "
                          "Using run_background() instead is encouraged to avoid blocking the interactive thread", 
                          category=InteractivePythonWarning)
            
        self._flask_app.run(host=host, port=port, threaded=threaded, debug=debug, **kwargs)    
    
    def run_background(self, host="127.0.0.1", port=1024, threaded=True, debug=False, hijack_port=True, **kwargs):
        """
        Starts the Flask application in a background thread.
        :param host: The hostname to listen on. Defaults to '127.0.0.1'.
        :param port: The port for the server. Defaults to 1024.
        :param threaded: Whether to handle each request in a separate thread. Defaults to True.
        :param debug: If set to True, provides a debug interface. Defaults to False.
        :param hijack_port: If set to True, attempts to stop any server running on the target port before starting a new one. Defaults to True.
        :param kwargs: Additional keyword arguments passed to Flask's run method.
        """
        if self.running:
            return

        kwargs = dict(kwargs)
        kwargs['use_reloader'] = False
        
        self._server_thread = threading.Thread(target=self.run, kwargs=dict(host=host, port=port, threaded=threaded, debug=False, hijack_port=hijack_port, **kwargs))
        self._server_thread.start()
        
        self._address = host
        self._port = port
            
    def stop(self, force=False):
        """
        Attempts to find and stop the running Flask server in this process.
        This is only useful in cases where the servers are running in background threads, 
        like for instance in jupyter instances.
        :param force: If True, forces the server to stop even if it's not detected as running.
        """
        if self.running or force:
            wsgis = [obj for obj in gc.get_objects() 
                     if isinstance(obj, BaseWSGIServer) and obj.server_address == (self.address, self.port)]

            for wsgi in wsgis:
                wsgi.shutdown()

            self._address = None
            self._port = None
            self._build_flask_app()
