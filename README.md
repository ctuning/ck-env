Fighting software and hardware chaos in research
================================================

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

Please, check [CK portable expeirmental workflows](https://github.com/ctuning/ck/wiki/Portable-workflows)
for more details!

Contributors
============
* General Motors and dividiti use CK to crowdsource benchmarking and optimization of CAFFE with different versions of compilers, libraries, models and data sets: [public CK repo](https://github.com/dividiti/ck-caffe)
* ARM and the cTuning foundation use CK to systematize SW/HW co-design: [HiPEAC Info'45 page 17](https://www.hipeac.net/assets/public/publications/newsletter/hipeacinfo45.pdf), [ARM TechCon'16 presentation and demo](http://schedule.armtechcon.com/session/know-your-workloads-design-more-efficient-systems), [public CK repo](https://github.com/ctuning/ck-wa)
* The community gradually provides description of all existing software in the CK format: [GitHub](https://github.com/ctuning/ck-env/tree/master/soft), [Wiki](https://github.com/ctuning/ck/wiki/Shared-soft-descriptions)
* The community gradually addes various packages to automatically rebuild software: [Wiki](https://github.com/ctuning/ck/wiki/Shared-packages)

License
=======
* BSD, 3-clause

Prerequisites
=============
* [Collective Knowledge Framework](http://github.com/ctuning/ck)

Installation
============

```
 $ (sudo) pip install ck
 $ ck pull repo:ck-env

 $ ck list soft
 $ ck list package

```

Usage
=====

You can easily detect and register in the CK all the instances of GCC and LLVM as following:
```
 $ ck detect soft:compiler.gcc
 $ ck detect soft:compiler.llvm
```

You can now see multiple versions of the detected software registered in the CK as following:
```
 $ ck show env
```

You can then compile and run unified CK benchmarks shared by the community using 
any of the above compiler instances (GCC, LLVM, ICC ...) and their versions simply as following:

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

![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)
