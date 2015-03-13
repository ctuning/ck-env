This is a Collective Knowledge Repository

Current status
==============
* Testing stage (stable, pre-release state) since 2015/02/13

Compatibility
=============
Linux, Windows, Android

Installation
============
* ck add repo:ck-env --shared --quiet

We suggest to add environment variable for CK package installations:

* Linux: export CK_TOOLS=[path]

* Windows: set CK_TOOLS=[path]

Update
======
* ck pull repo:ck-env

Description
===========
Researchers spend considerable amount of time connecting various
existing software together and then dealing with ever changing
versions, interfaces, API and environment. 

CK can serve as a proxy to existing or new software while 
automatically setting up environment for different versions,
checking dependencies, providing a unified interface to call them, 
and exchange information. 

Main modules are:

* env - setting up environment for existing software

* soft - registering various software and their versions 
in CK and automatically resolving dependencies. 

* package - unifying pakcage installation while automatically
resolving dependencies. 

* os - describing OS parameters

* platform* - detecting and unifying platform properties (features)


Note, that we already shared in this repo various software descriptions 
and packages from our past research (including compilers and libraries).

Other software descriptions and packages can be easily exchanged 
as CK repositories via GITHUB ...

This concept is described here: https://hal.inria.fr/hal-01054763

Further info: https://github.com/ctuning/ck-env/wiki


Dependencies
============

== Android ==

* adb

== Linux ==

* lspci

== Windows ==

* unzip.exe, tar.exe, gzip.exe, bzip2.exe


