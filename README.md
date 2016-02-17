Registering software environments in CK
=======================================

This is a relatively stable repository used to register
environment of various software in CK to let multiple
versions of different easily co-exist, automatically
resolve dependencies during tool installation, and
support experimentation with various versions of
tools. For example, we use it for autotuning with
different versions of LLVM, GCC, ICC, etc.

Authors
=======

* Grigori Fursin, cTuning foundation (France) / dividiti (UK)

License
=======
* BSD, 3-clause

Prerequisites
=============
* Collective Knowledge Framework: http://github.com/ctuning/ck

Installation
============

> ck pull repo:ck-env

Modules with actions
====================

env - software environments (to abstract multiple tools and their versions)

  * refresh - refresh environment setup (re-setup related software version)
  * resolve - resolve all dependencies for a given software
  * set - prepare and set environment for a given software
  * show - show all installed software environments

fgg.misc - auxiliary functions shared by Grigori Fursin

  * refresh_json - update json file
  * replace_string_in_file - replace string in a file

os - description of operating systems (OS)

  * find_close - find the most close description for the host OS

package - managing software packages (installing tools, registering in CK environments)

  * install - install CK package (download a tool if needed, install it, and register environment
  * setup - setup package (only register environment but do not install it)

platform - detecting and describing platforms

  * deinit - de-initialize device (put shared computational devices to powersave mode after experiments)
  * detect - detect various properties (features) of a given platform
  * exchange - exchange various information with a public server (for crowd-benchmarking/crow-tuning)
  * get_from_wmic - get information from WMIC tool on Windows
  * init_device - init remote device (useful when preparing shared computational device)

platform.gpu - describing and detecting platform GPU

  * detect - detect various properties (features) of a given GPU
  * set_freq - set frequency of a given acelerator (if supported)

platform.cpu - describing and detecting platform's CPUs

  * detect - detect various properties (features) of a given CPU
  * set_freq - set frequency of a given CPU (if supported)

platform.os - describing and detecting platform's operating systems

  * detect - detect various properties (features) of a host and target OS

script - scripts

  * run - run a given script (host OS dependent)

soft - managing software (registering in CK environment)

  * detect - detect version of a given software
  * setup - setup CK environment for a given software
