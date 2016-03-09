Create standalone ARM-based tool from Android NDK:
 $ build/tools/make-standalone-toolchain.sh --install-dir=/home/fursin/fggwork/android-llvm-3.6 --toolchain=arm-linux-androideabi-4.9 --llvm-version=3.6

 ck setup soft:compiler.llvm.android --target_os=android19-arm

Create standalone x86-based tool from Android NDK:
 $ build/tools/make-standalone-toolchain.sh --install-dir=/home/fursin/fggwork/android-llvm-3.6-x86 --toolchain=x86-4.9 --llvm-version=3.6

 ck setup soft:compiler.llvm.android --target_os=android19-x86

Create standalone x86_64-based tool from Android NDK:
 $ build/tools/make-standalone-toolchain.sh --install-dir=/home/fursin/fggwork/android-llvm-3.6-x86_64 --toolchain=x86_64-4.9 --llvm-version=3.6

 ck setup soft:compiler.llvm.android --target_os=android19-x86_64
