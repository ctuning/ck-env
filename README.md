Fighting software and hardware chaos in research
================================================

[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Linux & MacOS: [![Travis Build Status](https://travis-ci.org/ctuning/ck-env.svg?branch=master)](https://travis-ci.org/ctuning/ck-env)
Windows: [![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/github/ctuning/ck-env?branch=master&svg=true)](https://ci.appveyor.com/project/ens-lg4/ck-env)

This is a [Collective Knowledge](https://github.com/ctuning/ck) repository
with the functionality to support portable, customizable, reusable and automated workflows.
It lets users automatically detect the target platform with already installed software, data and models
required for a given workflow using [CK software detection plugins](https://codereef.ai/portal/c/soft)
and install missing [packages](https://codereef.ai/portal/c/package) in a unified way.
Multiple versions of code, data and models can now co-exist in a user or system environment
similar to Python virtualenv. 

Further info:
* [Open CodeReef platform to publish and download stable CK components](https://CodeReef.ai/portal/static/docs)
* [Documentation about portable CK workflows](https://github.com/ctuning/ck/wiki/Portable-workflows)
* [Shared portable CK program workflows](https://codereef.ai/portal/c/program)
* [Related CK publications](https://github.com/ctuning/ck/wiki/Publications)

Current maintainers
===================
* [dividiti](http://dividiti.com)

Authors
=======
* [Grigori Fursin](https://fursin.net) and the [cTuning foundation](https://cTuning.org)

Contributors
============
* See the list of [contributors](https://github.com/ctuning/ck-env/blob/master/CONTRIBUTIONS)

Installation
============

First install the CK framework as described [here](https://github.com/ctuning/ck#installation).

Then install this CK repository as follows:

```
 $ ck pull repo:ck-env

 $ ck list soft
 $ ck list package

```

Usage
=====

You can detect and register in the CK all the instances of GCC and LLVM as follows:
```
 $ ck detect soft:compiler.gcc
 $ ck detect soft:compiler.llvm
```

You can now see multiple versions of the detected software registered in the CK as follows:
```
 $ ck show env
```

You can then compile and run unified CK benchmarks shared by the community using 
any of the above compiler instances (GCC, LLVM, ICC ...) and their versions simply as follows:

```
 $ ck pull repo:ck-autotuning
 $ ck pull repo:ctuning-programs

 $ ck compile program:cbench-automotive-susan --speed
 $ ck run program:cbench-automotive-susan
```

If you have Android NDK and SDK installed, CK can automatically detect it together with compiler
versions (GCC, LLVM), register them and let you compile and run benchmarks on Android simply via:
```
 $ ck compile program:cbench-automotive-susan --speed --target_os=android21-arm-v7a
 $ ck run program:cbench-automotive-susan --target_os=android21-arm-v7a
```

You can find further details about our customizable and cross-platform package/environment manager
[here](https://github.com/ctuning/ck/wiki/Portable-workflows).


Questions and comments
======================

Please feel free to get in touch with the [CK community](https://github.com/ctuning/ck/wiki/Contacts) 
if you have any questions, suggestions and comments!
