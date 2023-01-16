# pyfallback

1. Use `Fallback` to wrap an object with fallback value.
2. Safely do stuff that possibly go wrong.
3. Use the `get()` method to retrieve result.

## Install

```bash
pip install pyfallback
```

## Usage

```python
from pyfallback import Fallback

# fallback
json = Fallback({"key": "value"}, fallback="fallback")
json["key"].get()  # "value"
json["bla"].get()  # "fallback"

# chaining
json = Fallback({"key": "1-2-3"}, fallback="4")
json["key"].split("-")[0].get()  # "1"
json["bla"].split("-")[0].get()  # "4"

# iterating
json = Fallback({"key": [1, 2, 3]}, fallback=[4, 5, 6])
[v.get() for v in json["key"]]  # [1, 2, 3]
[v.get() for v in json["bla"]]  # [4, 5, 6]

# see tests/test_fallback.py for more example 
```

## Contributing

Just submit a pull request :D <br />
Note: this project uses [poetry](https://github.com/python-poetry/poetry) and [pyenv](https://github.com/pyenv/pyenv).
