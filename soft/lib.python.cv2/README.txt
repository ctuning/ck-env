Supported automatic version detection starts from 4.3.0.38 onwards.


If you need to detect an earlier version, please create a version.py file
in the corresponding cv2/ directory with a single line:
------------->8--cut-here--8<-----------
opencv_version = "x.y.z.p"
------------->8--cut-here--8<-----------
where x.y.z.p is your desired version.


When installing older OpenCV versions please use --force_version:
    ck install package --tags=lib,python-package,cv2 --force_version=4.0.0.21
This will skip version detection.
