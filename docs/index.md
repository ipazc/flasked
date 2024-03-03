# Overview
{{project_name}} {{ version }} is an innovative Python package designed to enhance the Flask framework in order to ease the creation of API RESTful endpoints. This package allows developers to add, modify, and remove routes on-the-fly by introducing dynamic route management, making it ideal for interactive environments such as Jupyter notebooks or IPython sessions.

## Features

- **Dynamic Route Management**: Easily manage your application's routes without restarting the server.
- **Interactive Development**: Perfect for use in Jupyter notebooks, allowing for real-time testing and adjustments.
- **Typed Variables in Routes**: Define typed variables in your routes for more control and safety.

## Limitations

- **WSGI Compatibility**: While Flasked enhances development in interactive environments, deploying to production environments using WSGI servers like Gunicorn may not utilize all dynamic features, even though it is supported.
- **Security Considerations**: Dynamic route management, especially in production environments, requires careful consideration of security implications.

Flasked is released under the MIT license, allowing for flexibility in both personal and commercial projects.

## Installation

`Flasked` can be easily installed using pip, Python's package installer. Ensure you have pip installed and run the following command in your terminal:

```bash
pip install flasked
```

This command will download and install `Flasked` along with its dependencies, making it ready to use in your project.
