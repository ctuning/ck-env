# COCO API

This is the API of the COCO dataset: https://github.com/cocodataset/cocoapi.git

```
$ ck install package --tags=tool,coco
```

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

## Build warning
```
cythoning pycocotools/_mask.pyx to pycocotools/_mask.c
/usr/local/lib/python3.5/dist-packages/Cython/Compiler/Main.py:367: FutureWarning: Cython directive 'language_level' not set, using 2 for now (Py2). This will change in a later release! File: /home/anton/
CK_TOOLS/tool-coco-master-gcc-7.4.0-compiler.python-3.5.2-linux-64/src/PythonAPI/pycocotools/_mask.pyx
  tree = Parsing.p_module(s, pxd, full_module_name)
building 'pycocotools._mask' extension
```
