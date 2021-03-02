# COCO calibration datasets

This package takes the COCO 2017 training dataset with original JPEG images and
creates a calibration dataset according to one of the below options (CK
variations).

## Variations

### MLPerf Inference

This variation uses the [official MLPerf Inference calibration dataset](https://github.com/mlcommons/inference/blob/master/calibration/COCO/coco_cal_images_list.txt) (500 randomly selected images).

<pre>
&dollar; ck install package --tags=dataset,coco,calibration,mlperf
</pre>

### First 5

This variation uses the first five images of the MLPerf calibration dataset. 

<pre>
&dollar; ck install package --tags=dataset,coco,calibration,first.5
</pre>
