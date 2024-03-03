# Getting Started with Flasked

This guide will help you get started with Flasked, from instantiation to running your server and managing routes dynamically.

## Instantiating Flasked

Creating a Flasked application is straightforward. Simply import the `Flasked` class and create an instance:

```python
from flasked import Flasked

flasked = Flasked()
```

This instance is your gateway to dynamic route management and server control.

## Running the Server

Flasked simplifies server management with the ability to start the server in the background, perfect for interactive environments:

```python
flasked.run_background(host="127.0.0.1", port=1024)
```

It is possible to run the server at the beginning or at the end, no matter when, since the routes can be added dynamically to `flasked`. For interactive environments like Jupyter notebooks, it is encouraged to set it at the very beginning and then modify the routes on-the-fly.

If it is desired to block the thread, use `run()` instead of `run_background()`. Note that blocking the thread requires the routes to be defined beforehand.

### Versatile Port Handling

One of Flasked's key features is its ability to handle port conflicts gracefully. If Flasked detects another instance running on the same port, it will automatically stop the previous instance before starting a new one, ensuring your latest configuration is always running without manual intervention.

## Stopping the Server

Stopping the server is as easy as starting it. Just call the `stop` method:

```python
flasked.stop()
```

## Managing Routes

Flasked treats routes as dynamic entities that can be added, modified, or removed at runtime, similar to manipulating entries in a dictionary.

Note that setting routes can be done independently of the running status of `flasked`, that is, it works even *after* the server is running. However, it is encouraged to do so before `flasked` is running in case a WSGI server like Gunicorn or Tornado is going to deploy the app.

### Adding a Route

```python
class MyController:
    def get(self):
        return {"message": "Hello, Flasked!"}

flasked['/hello'] = MyController
```


### Modifying a Route

Simply reassign a new controller to an existing route path:

```python
class NewController:
    def get(self):
        return {"message": "New response"}

flasked['/hello'] = NewController
```

### Removing a Route

Remove a route as you would delete a key from a dictionary:

```python
del flasked['/hello']
```

## Summary

To view a summary of all defined routes and their methods, use the `.summary` property:

```python
flasked.summary
```

## Next Steps

Now that you're familiar with the basics of Flasked, explore more advanced features like handling typed variables in routes, stateful routes, and integrating Flasked with databases and other services. Flasked is designed to make your Flask development experience more interactive, flexible, and enjoyable.
