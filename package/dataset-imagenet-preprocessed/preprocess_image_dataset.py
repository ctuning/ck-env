#!/usr/bin/env python3

supported_extensions = ['jpeg', 'jpg', 'gif', 'png']

import os


# Zoom to target size
def resize_img(img, target_size):

  from scipy.ndimage import zoom

  zoom_w = float(target_size)/float(img.shape[0])
  zoom_h = float(target_size)/float(img.shape[1])
  return zoom(img, [zoom_w, zoom_h, 1])


# Crop the central region of the image
def crop_img(img, crop_percent):
  if crop_percent > 0 and crop_percent < 1.0:
    new_w = int(img.shape[0] * crop_percent)
    new_h = int(img.shape[1] * crop_percent)
    offset_w = int((img.shape[0] - new_w)/2)
    offset_h = int((img.shape[1] - new_h)/2)
    return img[offset_w:new_w+offset_w, offset_h:new_h+offset_h, :]
  else:
    return img


# Load and preprocess image
def load_image(image_path,            # Full path to processing image
               target_size,           # Desired size of resulting image
               intermediate_size = 0, # Scale to this size then crop to target size
               crop_percentage = 0,   # Crop to this percentage then scale to target size
               convert_to_bgr = False # Swap image channel RGB -> BGR
               ):

  import numpy as np
  import scipy.io

  img = scipy.misc.imread(image_path)

  # check if grayscale and convert to RGB
  if len(img.shape) == 2:
      img = np.dstack((img,img,img))

  # drop alpha-channel if present
  if img.shape[2] > 3:
      img = img[:,:,:3]

  # Resize and crop
  if intermediate_size > target_size:
    img = resize_img(img, intermediate_size)
    img = crop_img(img, float(target_size)/float(intermediate_size))
  elif crop_percentage > 0:
    img = crop_img(img, float(crop_percentage)/100.0)
    img = resize_img(img, target_size)

  # Convert to BGR
  if convert_to_bgr:
    swap_img = np.array(img)
    tmp_img = np.array(swap_img)
    tmp_img[:, :, 0] = swap_img[:, :, 2]
    tmp_img[:, :, 2] = swap_img[:, :, 0]
    img = tmp_img

  return img


def preprocess_directory(source_dir, destination_dir, crop_factor, square_side, inter_size, convert_to_bgr):
    "Go through the given directory and preprocess all the files"

    done_count = 0
    
    for filename in sorted(os.listdir(source_dir)):
        for extension in supported_extensions:
            if filename.lower().endswith( extension ):
                full_input_path     = os.path.join(source_dir, filename)
                full_output_path    = os.path.join(destination_dir, filename)

                image_data = load_image(image_path = full_input_path,
                                      target_size = square_side,
                                      intermediate_size = inter_size,
                                      crop_percentage = crop_factor,
                                      convert_to_bgr = convert_to_bgr)
                image_data.tofile(full_output_path)

                done_count += 1
                print("{}:  Stored {}".format(done_count, full_output_path) )


if __name__ == '__main__':
    import sys

    source_dir      = sys.argv[1]
    destination_dir = sys.argv[2]

    square_side     = int( os.environ['_INPUT_SQUARE_SIDE'] )
    crop_factor     = float( os.environ['_CROP_FACTOR'] )
    inter_size      = int( os.getenv('_INTERMEDIATE_SIZE', 0) )
    convert_to_bgr  = os.getenv('_CONVERT_TO_BGR', '').lower() == 'yes'

    print("From: {} , To: {} , Size: {} , Crop: {} , InterSize: {} , 2BGR: {}".format(source_dir, destination_dir, square_side, crop_factor, inter_size, convert_to_bgr) )

    preprocess_directory(source_dir, destination_dir, crop_factor, square_side, inter_size, convert_to_bgr)

