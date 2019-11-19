## Pre-requisites

* zip (`sudo apt install zip`)
* JDK (`sudo apt install openjdk-10-jdk-headless`)

## Known issues
```
rpi4@ ck install package --tags=tool,bazel,v1.1
...
ERROR: /tmp/bazel_hCQHVSZM/out/external/bazel_tools/tools/jdk/BUILD:499:1: Configurable attribute "actual" doesn't match this configuration: Could not find a JDK for host execution environment, please explicitly provide one using `--host_javabase.`
INFO: Call stack for the definition of repository 'remote_java_tools_linux' which is a http_archive (rule definition at /tmp/bazel_hCQHVSZM/out/external/bazel_tools/tools/build_defs/repo/http.bzl:292:16):
 - /tmp/bazel_hCQHVSZM/out/external/bazel_tools/tools/build_defs/repo/utils.bzl:205:9
 - /DEFAULT.WORKSPACE.SUFFIX:260:1
ERROR: Analysis of target '//src:bazel_nojdk' failed; build aborted:

/tmp/bazel_hCQHVSZM/out/external/bazel_tools/tools/jdk/BUILD:499:1: Configurable attribute "actual" doesn't match this configuration: Could not find a JDK for host execution environment, please explicitly provide one using `--host_javabase.`
INFO: Elapsed time: 19.580s
INFO: 0 processes.
FAILED: Build did NOT complete successfully (76 packages loaded, 412 targets 
```
