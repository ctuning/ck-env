# COCO API

This is the API of the COCO dataset: https://github.com/cocodataset/cocoapi.git

**NB:** Using Python 3 is recommended.

## Dependencies

- Setuptools.
- Cython (needed for compilation)
- NumPy (needed for compilation)
- Matplotlib (not needed for compilation)

We have no CK packages for some Python dependencies yet, so they should be installed
manually via `pip`:
```bash
$ python -m pip install setuptools
$ python -m pip install cython
```

**NB:** We now have `ck-env:package:lib-python-cython` but it does not correctly set up
path to the `cython` executable`.
