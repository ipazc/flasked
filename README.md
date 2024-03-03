# Flasked

![Flasked Badge](https://badge.fury.io/py/flasked.svg)

Flasked is an advanced Flask extension that brings unparalleled flexibility and ease to REST API development with Flask, particularly shining in dynamic environments like Jupyter notebooks. It empowers developers to dynamically manage routes without the need for server restarts, supports background server execution for seamless interactive development, and maintains compatibility with WSGI servers like Gunicorn for production deployments.

## Key Features

- **Dynamic Route Management**: Flasked allows for the dynamic addition, modification, and deletion of routes in real-time, eliminating the need for server restarts and enhancing the development workflow.
  
- **Background Server Execution**: Designed with interactive environments in mind, Flasked can run the server in the background, making it a perfect match for Jupyter notebooks and similar setups.
  
- **WSGI Compatibility**: While Flasked excels in development and testing environments, it is also fully compatible with WSGI servers, ensuring a smooth transition from development to production.

## Quick Start

### Installation

To install Flasked, simply run:

```bash
pip install flasked
```

### Creating Your First Route

1. **Instantiate Flasked**:

    ```python
    from flasked import Flasked

    flasked = Flasked()
    ```

2. **Run the Server in Background**:

    ```python
    flasked.run_background()
    ```

3. **Define a Route**:

    ```python
    class HelloWorld:
        def get(self):
            return {"message": "Hello, World!"}

    flasked['/'] = HelloWorld
    ```

4. **Access Your Route**:

    Open `http://127.0.0.1:1024/` in your browser to see the greeting message.

5. **Stop the Server** (optional):

    ```python
    flasked.stop()
    ```

## Documentation

For detailed documentation on Flasked's features, advanced routing options, and comprehensive examples, please refer to our [documentation](https://flasked.readthedocs.io/en/v0.1.0/).
Also, a [jupyter notebook](notebooks/demo_usage.ipynb) is available for learning more.

## Contributing

Contributions are warmly welcomed! Whether it's through submitting bug reports, feature requests, or pull requests, your input helps make Flasked better for everyone.

## License

Flasked is open-source software licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
