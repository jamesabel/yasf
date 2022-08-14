# yasf
Yet Another Structured Formatter

Function `sf` takes any number of positional or keyword arguments and attempts to turn them into a string.

## Usage

```python
from yasf import sf

s = sf("user", name="James", id=123)
print(s)  # 'user <> {"name": "James", "id": 123} <>'
```
