# CMake package

This package builds CMake from source for the following official releases:

* `v3.18.2` (default)
* `v3.17.4`

## Installation

To install a particular release, use one of the above variation tags e.g.:
```bash
$ ck install package --tags=tool,cmake,from.source,v3.18.2
```

### Build-thread variations

To limit the number of build threads on a resource-constrained platform, add e.g.:

```bash
$ ck install package --tags=tool,cmake,from.source,v3.18.2 \
--env.CK_HOST_CPU_NUMBER_OF_PROCESSORS=2
```
