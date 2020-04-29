# ImageNet calibration datasets

This package takes an ImageNet 2012 validation dataset with original JPEG
images (the full one with 50,000 images or a reduced one with the first 500
images of the full one - tagged "min") and creates a calibration dataset
according to one of the below options. A `val_map.txt` file gets generated too,
matching the file names and the class labels on the same line.

##  All 500 images of the "min" dataset

```bash
$ ck install package --tags=dataset,imagenet,all.500
```

## First 500 images (default)

```bash
$ ck install package --tags=dataset,imagenet,first.500
```

**NB:** Equivalent to `all.500` for the non-resized minimal dataset.

## MLPerf Inference option 1

```bash
$ ck install package --tags=dataset,imagenet,mlperf.option1
```

**NB:** This option was used for MLPerf Inference v0.5 by Intel and others. In fact, we use [Intel's file](https://github.com/mlperf/inference_results_v0.5/blob/master/closed/Intel/calibration/OV_RN-50-sample/imagenet_mlperf/converted_mlperf_list.txt), because [the official file](https://github.com/mlperf/inference/blob/master/calibration/ImageNet/cal_image_list_option_1.txt) does not have class labels.

## MLPerf Inference option 2

```bash
$ ck install package --tags=dataset,imagenet,mlperf.option2
```

**NB:** [The official file](https://github.com/mlperf/inference/blob/master/calibration/ImageNet/cal_image_list_option_2.txt) does have class labels in the second column (despite appearing to have just the increasing numbering).
