
Linux & MacOS: [![Travis Build Status](https://travis-ci.org/ctuning/ck-env.svg?branch=master)](https://travis-ci.org/ctuning/ck-env)
Windows: [![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/github/ctuning/ck-env?branch=master&svg=true)](https://ci.appveyor.com/project/ens-lg4/ck-env)

Fighting software and hardware chaos in research
================================================

[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-powered-by-ck.png)](http://cKnowledge.org)
[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)](http://cTuning.org)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

This is a [Collective Knowledge](https://github.com/ctuning/ck) repository
providing functionality for portable, customizable, eproducible and automated experimental workflows.
It lets users automatically detect multiple versions of different
software (compilers, libraries, tools, models, data sets) 
using [CK software detection plugins](http://cKnowledge.org/shared-soft-detection-plugins.html)
or install missing [packages](http://cKnowledge.org/shared-packages.html) 
in a unified way across diverse hardware with Linux, Windows, MacOS and Android operating systems.
It also allows users to collect information about a given platform in a unified way.

Further info:
* [First CK steps](https://github.com/ctuning/ck/wiki/First-steps)
* [CK portable experimental workflows](https://github.com/ctuning/ck/wiki/Portable-workflows)
* [CK documentation including "Getting Started Guide"](https://github.com/ctuning/ck/wiki)
  * [Reusable software detection plugins](http://cKnowledge.org/shared-soft-detection-plugins.html)
  * [Reusable CK packages to automate installation of workflows across diverse platforms](http://cKnowledge.org/shared-packages.html)
  * [Shared CK programs (workflows)](http://cKnowledge.org/shared-programs.html)
* [Reproducible SW/HW co-design competitions for deep learning and other emerging workloads using CK](http://cKnowledge.org/request)

Contributors
============
* General Motors and dividiti use CK to crowdsource benchmarking and optimization of deep learning with different versions of compilers, libraries, models and data sets: [public CK repo](https://github.com/dividiti/ck-caffe)
* ARM and the cTuning foundation use CK to systematize SW/HW co-design: [HiPEAC Info'45 page 17](https://www.hipeac.net/assets/public/publications/newsletter/hipeacinfo45.pdf), [ARM TechCon'16 presentation and demo](https://github.com/ctuning/ck/wiki/Demo-ARM-TechCon'16), [public CK repo](https://github.com/ctuning/ck-wa)

Acknowledgments
===============

[![logo](http://cKnowledge.org/images/logo-gm_resize.png)](http://gm.com)
[![logo](http://cKnowledge.org/images/logo-arm.png)](http://arm.com)
[![logo](http://cKnowledge.org/images/stfc-logo.jpg)](http://www.hartree.stfc.ac.uk)
[![logo](http://cKnowledge.org/images/logo-dividiti.png)](http://dividiti.com)
[![logo](http://cKnowledge.org/images/logo-microsoft.png)](https://www.microsoft.com/en-us/research)
[![logo](http://cKnowledge.org/images/logo-university-of-cambridge2.png)](https://www.cam.ac.uk)
[![logo](http://cKnowledge.org/images/logo-pitt.png)](http://www.pitt.edu)
[![logo](http://cKnowledge.org/images/logo-imperial2.png)](https://www.imperial.ac.uk)
[![logo](http://cKnowledge.org/images/logo-university-of-edinburgh2.png)](http://www.ed.ac.uk)
[![logo](http://cKnowledge.org/images/logo_tetracom_resized.png)](http://tetracom.eu)
[![logo](http://cKnowledge.org/images/logo-rpi.png)](https://www.raspberrypi.org)
[![logo](http://cKnowledge.org/images/logo-xored.jpg)](http://xored.com)
[![logo](http://cKnowledge.org/images/CTuning_foundation_logo2.png)](http://cTuning.org)

License
=======
* BSD, 3-clause

Minimal CK installation
=======================

The minimal installation requires:

* Python 2.7 or 3.3+ (limitation is mainly due to unitests)
* Git command line client.

### Linux/MacOS

You can install CK in your local user space as follows:

```
$ git clone http://github.com/ctuning/ck
$ export PATH=$PWD/ck/bin:$PATH
$ export PYTHONPATH=$PWD/ck:$PYTHONPATH
```

You can also install CK via PIP with sudo to avoid setting up environment variables yourself:

```
$ sudo pip install ck
```

### Windows

First you need to download and install a few dependencies from the following sites:

* Git: https://git-for-windows.github.io
* Minimal Python: https://www.python.org/downloads/windows

You can then install CK as follows:
```
 $ pip install ck
```

or


```
 $ git clone https://github.com/ctuning/ck.git ck-master
 $ set PATH={CURRENT PATH}\ck-master\bin;%PATH%
 $ set PYTHONPATH={CURRENT PATH}\ck-master;%PYTHONPATH%
```

Installation of a CK workflow for virtual environments and packages
===================================================================

```
 $ ck pull repo:ck-env

 $ ck list soft
 $ ck list package

```

Usage
=====

You can easily detect and register in the CK all the instances of GCC and LLVM as follows:
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

Publications
============

The concepts have been described in the following publications:

```
@inproceedings{ck-date16,
    title = {{Collective Knowledge}: towards {R\&D} sustainability},
    author = {Fursin, Grigori and Lokhmotov, Anton and Plowman, Ed},
    booktitle = {Proceedings of the Conference on Design, Automation and Test in Europe (DATE'16)},
    year = {2016},
    month = {March},
    url = {https://www.researchgate.net/publication/304010295_Collective_Knowledge_Towards_RD_Sustainability}
}
```

All CK-related publications: [link](https://github.com/ctuning/ck/wiki/Publications)

Questions and comments
======================

You are welcome to get in touch with the [CK community](https://github.com/ctuning/ck/wiki/Contacts) if you have questions or comments!
