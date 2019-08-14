## Installation

```
$ ck install package --tags=dataset,imagenet,preprocessed,using-opencv
```

## Details

#### Summary of preprocessing methods

The table below summarizes the available methods.

| Preprocessing method    | OpenCV universal  | OpenCV for ResNet | OpenCV for MobileNet |
|-|-|-|-|
| Additional tags         | `universal`       | `for-resnet`      | `for-mobilenet`      |
| Supported models        | ResNet, MobileNet | ResNet only       | MobileNet only       |
| Supported platforms     | x86i              | x86               | x86                  |
| Data format             | rgb8 (int8)       | rgbf32 (float32)  | rgbf32 (float32)     |
| Data size               | 7.1G              | 29G               | 29G                  |



#### Accuracy on the ImageNet 2012 validation set

The table below shows the accuracy on the ImageNet 2012 validation set
(50,000 images) of the MLPerf Inference v0.5 image classification models measured
- [via TensorFlow (C++)](https://github.com/mlperf/inference/tree/master/v0.5/classification_and_detection/optional_harness_ck/classification/tf-cpp).

| Model                   | Metric | OpenCV universal | OpenCV for ResNet | OpenCV for MobileNet |
|-|-|-|-|-|
| ResNet                  |  Top1  | 0.76442          | 0.76456           | N/A                  |
|                         |  Top5  | 0.93074          | 0.93016           | N/A                  |
| MobileNet non-quantized |  Top1  | 0.71676          | N/A               | 0.71676              |
|                         |  Top5  | 0.90118          | N/A               | 0.90118              |
| MobileNet quantized     |  Top1  | 0.70700          | N/A               | 0.70694              |
|                         |  Top5  | 0.89594          | N/A               | 0.89594              |

- [via TFLite](https://github.com/mlperf/inference/tree/master/v0.5/classification_and_detection/optional_harness_ck/classification/tflite).

| Model                   | Metric | OpenCV universal | OpenCV for ResNet | OpenCV for MobileNet |
|-|-|-|-|-|
| ResNet                  |  Top1  | 0.76442          | 0.76456           | N/A                  |
|                         |  Top5  | 0.93074          | 0.93016           | N/A                  |
| MobileNet non-quantized |  Top1  | 0.71676          | N/A               | 0.71676              |
|                         |  Top5  | 0.90118          | N/A               | 0.90118              |
| MobileNet quantized     |  Top1  | 0.70762          | N/A               | N/A (bug?)           |
|                         |  Top5  | 0.89266          | N/A               | N/A (bug?)           |
