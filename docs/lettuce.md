!!! Warning
    Lettuce has a [bug](https://github.com/gabrielfalcao/lettuce/issues/464) which
    doesn't allow you to use it with `cli-bdd` yet. When the bug is fixed we will
    turn on functional test in `tests/functional/lettuce/tests.py`.

`cli-bdd` could be used with [lettuce](http://lettuce.it/) (not yet).

# Steps

In your lettuce steps module import all the steps from `cli-bdd`:

```python
from cli_bdd.lettuce.steps import *
```

That's it. Now you can use all the steps in your scenarios.
