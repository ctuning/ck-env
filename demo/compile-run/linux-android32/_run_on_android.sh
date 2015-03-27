adb push a.out /data/local/tmp/a.out
adb push data.pgm /data/local/tmp/data.pgm

adb shell "cd /data/local/tmp; rm data.out.pgm; chmod 0755 a.out; export CT_REPEAT_MAIN=10; ./a.out data.pgm data.out.pgm -e"

adb pull /data/local/tmp/data.out.pgm data.out.pgm
