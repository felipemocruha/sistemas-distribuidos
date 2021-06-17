from functools import wraps
from random import random

from flask import jsonify


def inject_failures(percentage):
    def middleware(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            if random() > percentage:
                return handler(*args, **kwargs)
            return jsonify({'error': 'Internal Server Error'}), 500

        return wrapper

    return middleware
