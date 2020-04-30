# ImageNet calibration datasets

This package takes an ImageNet 2012 validation dataset with original JPEG
images (the full one with 50,000 images or a reduced one with the first 500
images of the full one - tagged "min") and creates a calibration dataset
according to one of the below options (CK variations). A `val_map.txt` file gets generated too,
matching the file names and the class labels on the same line.

## Accuracy with [OpenVINO "pre-release"](https://github.com/openvinotoolkit/openvino/tree/pre-release)

| Model     | Number of images | Calibration option | Top 1 accuracy | Ranking for each group of 3 |
| -         | -                |  -                 | -              | -       |
| MobileNet | 500              | `first.500`        | 72.800%        | 1       |
| MobileNet | 500              | `mlperf.option1`   | 72.400%        | 3       |
| MobileNet | 500              | `mlperf.option2`   | 72.600%        | 2       |
| MobileNet | 50,000           | `first.500`        | 71.466%        | 2       |
| MobileNet | 50,000           | `mlperf.option1`   | 71.460%        | 3       |
| MobileNet | 50,000           | `mlperf.option2`   | 71.500%        | 1       |
| ResNet    | 500              | `first.500`        | 75.600%        | 2       |
| ResNet    | 500              | `mlperf.option1`   | 75.400%        | 3       |
| ResNet    | 500              | `mlperf.option2`   | 76.000%        | 1       |
| ResNet    | 50,000           | `first.500`        | 76.268%        | 1       |
| ResNet    | 50,000           | `mlperf.option1`   | 76.226%        | 2       |
| ResNet    | 50,000           | `mlperf.option2`   | 76.160%        | 3       |

**NB:** For official MLPerf Inference submissions on 50,000 images,
`mlperf.option2` should be used for MobileNet and `mlperf.option1` should be
used for ResNet. Surprisingly, `first.500` is never the worst, and is actually
the best for ResNet on 50,000 images.

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


### Unit-tests

```bash
$ ck install package --tags=dataset,imagenet,first.1
$ ck install package --tags=dataset,imagenet,first.5
$ ck install package --tags=dataset,imagenet,first.1.dup.5
```

**NB:** `first.1` and `first.5` use a file list (with the first and the first 5
images, respectively) with a file name but without a class label.
`first.1.dup.5` duplicates the same file name 5 times.

#### Accuracy with [OpenVINO "pre-release"](https://github.com/openvinotoolkit/openvino/tree/pre-release)

| Model     | Number of images | Calibration option | Top 1 accuracy |
| -         | -                |  -                 | -              |
| MobileNet | 500              | `first.1`          | 37.200%        |
| MobileNet | 500              | `first.1.dup.5`    | 37.200%        |
| MobileNet | 500              | `first.5`          | 70.800%        |
| ResNet    | 500              | `first.1`          | 74.200%        |
| ResNet    | 500              | `first.1.dup.5`    | 74.200%        |
| ResNet    | 500              | `first.5`          | 75.800%        |
