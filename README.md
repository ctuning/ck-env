***Note that this repository is outdated: we are now using the next generation of the MLCommons CK workflow automation meta-framework (Collective Mind aka CM) developed by the [open working group](https://github.com/mlcommons/ck/blob/master/docs/mlperf-education-workgroup.md). Feel free to [join this community effort](https://forms.gle/i5gCDtBC8gMtcvRw6) to learn how to modularize ML Systems and automate their benchmarking, optimization and deployment in the real world!***

Fighting the software and hardware chaos
========================================

**All CK components for AI and ML are now collected in [one repository](https://github.com/ctuning/ck-mlops)!**

*This project is hosted by the [cTuning foundation (non-profit R&D organization)](https://cTuning.org).*

[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Linux & MacOS: [![Travis Build Status](https://travis-ci.org/ctuning/ck-env.svg?branch=master)](https://travis-ci.org/ctuning/ck-env)
Windows: [![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/github/ctuning/ck-env?branch=master&svg=true)](https://ci.appveyor.com/project/ens-lg4/ck-env)

This is a [Collective Knowledge](https://github.com/ctuning/ck) repository
with the functionality to support portable, customizable, reusable and automated workflows.
It lets users automatically detect the target platform with already installed software, data and models
required for a given workflow using [CK software detection plugins](https://cKnowledge.io/c/soft)
and install missing [packages](https://cKnowledge.io/c/package) in a unified way.
Multiple versions of code, data and models can now co-exist in a user or system environment
similar to Python virtualenv. 

Further info:
* [Open CK platform to publish and download stable CK components](https://cKnowledge.io)
* [Documentation about portable CK workflows](https://github.com/ctuning/ck/wiki/Portable-workflows)
* [Reproducible program workflows](https://cKnowledge.io/c/program)
* [Related CK publications](https://github.com/ctuning/ck/wiki/Publications)

Author
======
* [Grigori Fursin](https://fursin.net)

Contributors
============
* See the list of [contributors](https://github.com/ctuning/ck-env/blob/master/CONTRIBUTIONS)

Shared CK modules with actions
==============================

* [apk](https://cKnowledge.io/c/module/apk)
* [artifact](https://cKnowledge.io/c/module/artifact)
* [crowdnode](https://cKnowledge.io/c/module/crowdnode)
* [device](https://cKnowledge.io/c/module/device)
* [env](https://cKnowledge.io/c/module/env)
* [log](https://cKnowledge.io/c/module/log)
* [machine](https://cKnowledge.io/c/module/machine)
* [me](https://cKnowledge.io/c/module/me)
* [misc](https://cKnowledge.io/c/module/misc)
* [os](https://cKnowledge.io/c/module/os)
* [package](https://cKnowledge.io/c/module/package)
* [platform](https://cKnowledge.io/c/module/platform)
* [platform.cpu](https://cKnowledge.io/c/module/platform.cpu)
* [platform.dsp](https://cKnowledge.io/c/module/platform.dsp)
* [platform.gpu](https://cKnowledge.io/c/module/platform.gpu)
* [platform.init](https://cKnowledge.io/c/module/platform.init)
* [platform.nn](https://cKnowledge.io/c/module/platform.nn)
* [platform.npu](https://cKnowledge.io/c/module/platform.npu)
* [platform.os](https://cKnowledge.io/c/module/platform.os)
* [result](https://cKnowledge.io/c/module/result)
* [script](https://cKnowledge.io/c/module/script)
* [soft](https://cKnowledge.io/c/module/soft)
* [xml](https://cKnowledge.io/c/module/xml)

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
