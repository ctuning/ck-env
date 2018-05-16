Fighting software and hardware chaos in research
================================================

*Feel free to provide your favorite software descriptions (see examples [here](https://github.com/ctuning/ck-env/tree/master/soft)).*
*Do not hesitate to ask for instructions and help [here](https://groups.google.com/forum/#!forum/collective-knowledge)!*

[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-powered-by-ck.png)](http://cKnowledge.org)
[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)](http://cTuning.org)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Researchers nowadays suffer from continuously changing
software and hardware stack when sharing, customizing
and reproducing experimental results:

![SW/HW chaos](https://github.com/ctuning/ck-guide-images/blob/master/image-mess.png)

This is an extension repository to the [Collective Knowledge Framework](https://github.com/ctuning/ck)
to let users automatically detect or install multiple versions of various software
(compilers, libraries, tools, models, data sets) 
across diverse hardware with Linux, Windows, MacOS and Android operating systems.
This, in turn, allows researchers implement portable, customizable and reproducible experimental workflows
as described [here](https://github.com/ctuning/ck/wiki/Portable-workflows).

The community gradually describes various software using [CK entries](https://github.com/ctuning/ck-env/tree/master/soft) 
with JSON meta and simple Python scripts to detect coexisting installations. 
See already shared [software descriptions](https://github.com/ctuning/ck/wiki/Shared-soft-descriptions)
and [package descriptions](https://github.com/ctuning/ck/wiki/Shared-packages).

Please, check [CK portable experimental workflows](https://github.com/ctuning/ck/wiki/Portable-workflows)
for more details!

Contributors
============
* General Motors and dividiti use CK to crowdsource benchmarking and optimization of CAFFE with different versions of compilers, libraries, models and data sets: [public CK repo](https://github.com/dividiti/ck-caffe)
* ARM and the cTuning foundation use CK to systematize SW/HW co-design: [HiPEAC Info'45 page 17](https://www.hipeac.net/assets/public/publications/newsletter/hipeacinfo45.pdf), [ARM TechCon'16 presentation and demo](https://github.com/ctuning/ck/wiki/Demo-ARM-TechCon'16), [public CK repo](https://github.com/ctuning/ck-wa)
* The community gradually provides description of all existing software in the CK format: [GitHub](https://github.com/ctuning/ck-env/tree/master/soft), [Wiki](https://github.com/ctuning/ck/wiki/Shared-soft-descriptions)
* The community gradually adds various packages to automatically rebuild software: [Wiki](https://github.com/ctuning/ck/wiki/Shared-packages)

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

* http://tinyurl.com/zyupd5v (DATE'16)
* http://arxiv.org/abs/1506.06256 (CPC'15)
* http://hal.inria.fr/hal-01054763 (Journal of Scientific Programming'14)
* https://hal.inria.fr/inria-00436029 (GCC Summit'09)

Feedback
========
* https://groups.google.com/forum/#!forum/collective-knowledge
