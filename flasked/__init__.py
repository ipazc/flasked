#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#MIT License
#
#Copyright (c) 2017 Iván de Paz Centeno
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


from flask import Flask
from flask_restful import Api, Resource

__author__ = 'Iván de Paz Centeno'


class Flasked(object):

    def __init__(self):
        self.flask_app = Flask(__name__)
        self.api = Api(self.flask_app)
        self.routes = {}

    def __len__(self):
        return len(self.routes)

    def __setitem__(self, key, value):
        args = []; kwargs = {}

        if type(value) is tuple and len(value) > 1:
            parent = value[0]

            if len(value) == 2 and type(value[-1]) is dict:
                d = value[-1]

                is_args_dict = False

                if 'args' in d:
                    args = d['args']
                    is_args_dict = True

                if 'kwargs' in d:
                    kwargs = d['kwargs']
                    is_args_dict = True

                if not is_args_dict:
                    args.append(d)
            else:
                for arg in value[1:]:
                    args.append(arg)

        else:
            parent = value

        class Generic(Resource, parent):
            _args = args
            _kwargs = kwargs
            def __init__(self):
                Resource.__init__(self)
                parent.__init__(self, *self._args, **self._kwargs)

        if key in self.api.resources:
            self.api.resources.remove(key)

        self.api.add_resource(Generic, key)
        self.routes[key] = Generic

    def __getitem__(self, key):
        return self.routes[key]

    def __contains__(self, item):
        return item in self.routes

    def items(self):
        return self.routes.items()

    def keys(self):
        return self.routes.keys()

    def values(self):
        return self.routes.values()

    def run(self, host="localhost", port=1025, threaded=True, debug=False, **kwargs):
        self.flask_app.run(host=host, port=port, threaded=threaded, debug=debug, **kwargs)

    def __repr__(self):
        return "API, {} endpoint handlers".format(len(self))

    def __str__(self):
        return "API, {} endpoint handlers".format(len(self))
