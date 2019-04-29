Some tests on full 50000 ImageNet validation set
using MobileNet model and ONNX runtime,
in different pre-processing modes:

----------------------------
guentherized.1,crop.1000

"accuracy_top1": 0.6609,
"accuracy_top5": 0.86576,
----------------------------
guentherized.0,crop.1000:

"accuracy_top1": 0.67698,
"accuracy_top5": 0.87812,
----------------------------
guentherized.1,crop.875:

"accuracy_top1": 0.67938,
"accuracy_top5": 0.87506,
----------------------------
guentherized.2,crop.1000:

"accuracy_top1": 0.68648,
"accuracy_top5": 0.88548,
----------------------------
guentherized.2,crop.875:

"accuracy_top1": 0.69598,
"accuracy_top5": 0.8901,
----------------------------
guentherized.0,crop.875:

"accuracy_top1": 0.69968,
"accuracy_top5": 0.89366,
----------------------------


Creating single-image datasets (need disambiguation in filename, extra tags and extra path) :
    ck install package --tags=dataset,preprocessed,external_file --env.CK_IMAGE_FILE=~/Desktop/lenny_kite.JPG --extra_tags=lenny_kite --extra_path=_lenny_kite
    ck install package --tags=dataset,preprocessed,external_file --env.CK_IMAGE_FILE=~/Desktop/lenny_canopy.JPG --extra_tags=lenny_canopy --extra_path=_lenny_canopy
