all:
	# install pycocotools locally
	${CK_ENV_COMPILER_PYTHON_FILE} setup.py build_ext --inplace
	rm -rf build

install:
	# install pycocotools to the Python site-packages
	${CK_ENV_COMPILER_PYTHON_FILE} setup.py build_ext install
	rm -rf build
