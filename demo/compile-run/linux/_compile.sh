. ./_clean.sh

ck set env tags=compiler,lang-c bat_file=tmp-ck-env.sh --bat_new --print && . ./tmp-ck-env.sh && rm tmp-ck-env.sh || exit 1

$CK_CC $CK_COMPILER_FLAGS_OBLIGATORY ctuning-rtl.c susan.c ${CK_FLAGS_OUTPUT}a.out $CK_LD_FLAGS_EXTRA -lm
$CK_OBJDUMP a.out > a.lst
