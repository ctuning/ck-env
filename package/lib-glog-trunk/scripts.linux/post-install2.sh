cd ${INSTALL_DIR}/install

if [ -d "lib64" ] && ! [ -d "lib" ]; then
    ln -s lib64 lib
fi
