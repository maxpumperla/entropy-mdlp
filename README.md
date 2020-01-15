# entropy-mdlp

Minimum description length principle algorithm in python, for optimal binning of continuous variables. This
package is a port of the respective R package of the same name. Install with

```bash_script
pip install entropymdlp
```

and then run an example like so:

```python
from entropymdlp.mdlp import MDLP
mdlp = MDLP()

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
```

The function will return the index of this point and the respective entropy.

```python
print(mdlp.find_cut_index(x, y))
```
