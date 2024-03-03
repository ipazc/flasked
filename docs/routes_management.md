# Route Management

Flasked revolutionizes route management in Flask applications by introducing the ability to dynamically add, modify, and remove routes. This flexibility is particularly useful in interactive development environments.

## Adding Routes

To add a route, simply assign a controller class to a route pattern:

```python
class RootController:
    def get(self):
        return {"result": "GET response"}

flasked['/'] = RootController
```

This will create a route at the root (`/`) that responds to GET requests with a JSON response.

## Modifying Routes

Routes can be modified on-the-fly by reassigning a different controller to the same route pattern:

```python
class NewRootController:
    def get(self):
        return {"result": "New GET response"}
    
    def post(self):
        return {"result": "New POST response"}
      
flasked['/'] = NewRootController
```

This instantly updates the route to use the new controller without restarting the server.

## Removing Routes

To remove a route, simply delete it from the Flasked instance:

```python
del flasked['/']
```

This immediately removes the route from the application.

## Advanced Routing

Flasked supports advanced routing features, including:

- **Typed Variables**: Define typed variables in routes to automatically parse and validate parameters. Available types are `[int, float, string]`

    ```python
    class TypedController:
        def get(self, id: int):
            return {"id": id}

    flasked['/item/<int:id>'] = TypedController
    ```

- **Path Variables**: Capture segments of the URL path as variables.

    ```python
    class PathController:
        def get(self, path_variable):
            return {"path": path_variable}

    flasked['/path/<path:path_variable>'] = PathController
    ```

- **Query Parameters**: Access query parameters directly in your controller methods using `request.args`.

    ```python
    from flask import request
  
    class QueryController:
        def get(self):
            param = request.args.get('param')
            return {"param": param}

    flasked['/query'] = QueryController
    ```

- **JSON Requests**: Handle JSON data seamlessly in your controller methods.

    ```python
    from flask import request
  
    class JSONController:
        def post(self):
            data = request.get_json()
            return {"received": data}

    flasked['/json'] = JSONController
    ```

These examples illustrate the power and flexibility of Flasked's route management, making it an invaluable tool for rapid development and testing in interactive environments.
