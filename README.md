# pyfallback

## Install
> pip install fallback

## Usage

```python
from pyfallback import Fallback

json = {
    'attr-1': 'value-1',
}
json = Fallback(json, fallback="default")

# fallback
json["attr-1"].get()  # "value1"
json["attr-2"].get()  # "default"

# chaining
json["attr-1"].split('-')[0].get()  # "value"

# see tests/test_fallback.py for more example 
```

## Contributing
Just submit a pull request :D <br />
Note: this project uses poetry and pyenv
