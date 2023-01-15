# pyfallback

Provide a simple Fallback class that wraps an object, any operations that fails will use/return specified fallback.

## Install

```bash
pip install pyfallback
```

## Usage

```python
from pyfallback import Fallback

json = Fallback({'attr-1': 'value-1'}, fallback="fallback")

# fallback
json["attr-1"].get()  # "value1"
json["attr-2"].get()  # "fallback"

# chaining
json["attr-1"].split('-')[0].get()  # "value"

# see tests/test_fallback.py for more example 
```

## Contributing

Just submit a pull request :D <br />
Note: this project uses [poetry](https://github.com/python-poetry/poetry) and [pyenv](https://github.com/pyenv/pyenv).
