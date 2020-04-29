# ImageNet calibration datasets

This package takes an ImageNet 2012 validation dataset with original JPEG
images (the full one with 50,000 images or a reduced one with the first 500
images of the full one - tagged "min") and creates a calibration dataset
according to one of the below options (CK variations). A `val_map.txt` file gets generated too,
matching the file names and the class labels on the same line.

## Accuracy with [OpenVINO "pre-release"](https://github.com/openvinotoolkit/openvino/tree/pre-release)

| Model     | Number of images |Calibration option |  Top 1 accuracy |
| -         | -                | -                 | -               | 
| MobileNet | 500              |`first.500`        |  72.800%        |
| MobileNet | 500              |`mlperf.option1`   |  72.400%        |
| MobileNet | 500              |`mlperf.option2`   |  72.600%        |
| MobileNet | 50,000           |`first.500`        |  -              |
| MobileNet | 50,000           |`mlperf.option1`   |  -              |
| MobileNet | 50,000           |`mlperf.option2`   |  -              |
| ResNet    | 500              |`first.500`        |  75.600%        |
| ResNet    | 500              |`mlperf.option1`   |  -              |
| ResNet    | 500              |`mlperf.option2`   |  -              |
| ResNet    | 50,000           |`first.500`        |  76.268%        |
| ResNet    | 50,000           |`mlperf.option1`   |  -              |
| ResNet    | 50,000           |`mlperf.option2`   |  -              |


## Variations

###  All 500 images of the "min" dataset

```bash
$ ck install package --tags=dataset,imagenet,all.500
```

### First 500 images (default)

```bash
$ ck install package --tags=dataset,imagenet,first.500
```

**NB:** Equivalent to `all.500` for the "min" dataset.

### MLPerf Inference option 1

```bash
$ ck install package --tags=dataset,imagenet,mlperf.option1
```

**NB:** This option was used for MLPerf Inference v0.5 by Intel and others. In fact, we use [Intel's file](https://github.com/mlperf/inference_results_v0.5/blob/master/closed/Intel/calibration/OV_RN-50-sample/imagenet_mlperf/converted_mlperf_list.txt), because [the official file](https://github.com/mlperf/inference/blob/master/calibration/ImageNet/cal_image_list_option_1.txt) does not have class labels.


### MLPerf Inference option 2

```bash
$ ck install package --tags=dataset,imagenet,mlperf.option2
```

**NB:** [The official file](https://github.com/mlperf/inference/blob/master/calibration/ImageNet/cal_image_list_option_2.txt) does have class labels in the second column (despite appearing to have just the increasing numbering).
