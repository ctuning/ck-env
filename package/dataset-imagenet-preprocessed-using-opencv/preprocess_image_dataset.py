#!/usr/bin/env python3

supported_extensions = ['jpeg', 'jpg', 'gif', 'png']

import os
import cv2
import numpy as np

# Load and preprocess image
def load_image(image_path,            # Full path to processing image
               target_size,           # Desired size of resulting image
               intermediate_size = 0, # Scale to this size then crop to target size
               crop_percentage = 87.5,# Crop to this percentage then scale to target size
               data_type = 'uint8',   # Data type to store
               convert_to_bgr = False,# Swap image channel RGB -> BGR
               audit_test03 = False,  # Wipe out the zero-th channel of the image
               interpolation_method = cv2.INTER_LINEAR # Interpolation method.
               ):

    out_height = target_size
    out_width  = target_size

    def resize_with_aspectratio(img):
        height, width, _ = img.shape
        new_height = int(100. * out_height / crop_percentage)   # intermediate oversized image from which to crop
        new_width = int(100. * out_width / crop_percentage)     # ---------------------- ,, ---------------------
        if height > width:
            w = new_width
            h = int(new_height * height / width)
        else:
            h = new_height
            w = int(new_width * width / height)
        img = cv2.resize(img, (w, h), interpolation = interpolation_method)
        return img

    def center_crop(img):
        height, width, _ = img.shape
        left = int((width - out_width) / 2)
        right = int((width + out_width) / 2)
        top = int((height - out_height) / 2)
        bottom = int((height + out_height) / 2)
        img = img[top:bottom, left:right]
        return img


    img = cv2.imread(image_path)

    if audit_test03:    # NB: since Grayscale images only have a single channel, this operation will wipe the whole image
        img[:,:,0] = 0

    if len(img.shape) < 3 or img.shape[2] != 3:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Mimic preprocessing steps from the official reference code.
    img = resize_with_aspectratio(img)
    img = center_crop(img)

    # Convert to BGR.
    if convert_to_bgr:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    return img


def preprocess_files(selected_filenames, source_dir, destination_dir, crop_percentage, square_side, inter_size, convert_to_bgr, audit_test03,
    data_type, new_file_extension, normalize_data, subtract_mean, given_channel_means, interpolation_method):
    "Go through the selected_filenames and preprocess all the files (optionally normalize and subtract mean)"

    output_filenames = []

    for current_idx in range(len(selected_filenames)):
        input_filename = selected_filenames[current_idx]

        full_input_path = os.path.join(source_dir, input_filename)

        image_data = load_image(image_path = full_input_path,
                              target_size = square_side,
                              intermediate_size = inter_size,
                              crop_percentage = crop_percentage,
                              data_type = data_type,
                              convert_to_bgr = convert_to_bgr,
                              audit_test03 = audit_test03,
                              interpolation_method = interpolation_method)

        image_data = np.asarray(image_data, dtype=data_type)

        # Normalize.
        if normalize_data:
            image_data = image_data/127.5 - 1.0

        # Subtract mean value.
        if subtract_mean:
            if len(given_channel_means):
                image_data -= given_channel_means
            else:
                image_data -= np.mean(image_data)

        output_filename = input_filename.rsplit('.', 1)[0] + '.' + new_file_extension if new_file_extension else input_filename

        full_output_path = os.path.join(destination_dir, output_filename)
        image_data.tofile(full_output_path)

        print("[{}]:  Stored {}".format(current_idx+1, full_output_path) )

        output_filenames.append(output_filename)

    return output_filenames


if __name__ == '__main__':
    import sys

    source_dir              = sys.argv[1]   # ignored if CK_IMAGE_FILE points to a file
    destination_dir         = sys.argv[2]

    square_side             = int( os.environ['_INPUT_SQUARE_SIDE'] )
    crop_percentage         = float( os.environ['_CROP_FACTOR'] )
    inter_size              = int( os.getenv('_INTERMEDIATE_SIZE', 0) )
    convert_to_bgr          = os.getenv('_CONVERT_TO_BGR', '').lower() in ('yes', 'true', 'on', '1')
    audit_test03            = os.getenv('_AUDIT_TEST03', '').lower() in ('yes', 'true', 'on', '1')
    offset                  = int( os.getenv('_SUBSET_OFFSET', 0) )
    volume_str              = os.getenv('_SUBSET_VOLUME', '' )
    fof_name                = os.getenv('_SUBSET_FOF', '')
    data_type               = os.getenv('_DATA_TYPE', '')
    new_file_extension      = os.getenv('_NEW_EXTENSION', '')
    normalize_data          = os.getenv('_NORMALIZE_DATA', '').lower() in ('yes', 'true', 'on', '1')
    subtract_mean           = os.getenv('_SUBTRACT_MEAN', '').lower() in ('yes', 'true', 'on', '1')
    given_channel_means     = os.getenv('_GIVEN_CHANNEL_MEANS', '')
    if given_channel_means:
        given_channel_means = [ float(x) for x in given_channel_means.split(' ') ]

    interpolation_method    = os.getenv('_INTERPOLATION_METHOD', '')

    image_file              = os.getenv('CK_IMAGE_FILE', '')

    print(("From: {} , To: {} , Size: {} , Crop: {} , InterSize: {} , 2BGR: {}, AUD: {}, OFF: {}, VOL: '{}', FOF: {},"+
        " DTYPE: {}, EXT: {}, NORM: {}, SMEAN: {}, GCM: {}, INTER: {}, IMG: {}").format(
        source_dir, destination_dir, square_side, crop_percentage, inter_size, convert_to_bgr, audit_test03, offset, volume_str, fof_name,
        data_type, new_file_extension, normalize_data, subtract_mean, given_channel_means, interpolation_method, image_file) )

    if interpolation_method == 'INTER_AREA':
        # Used for ResNet in pre_process_vgg.
        interpolation_method = cv2.INTER_AREA
    else:
        # Default interpolation method.
        interpolation_method = cv2.INTER_LINEAR

    if image_file:
        source_dir          = os.path.dirname(image_file)
        selected_filenames  = [ os.path.basename(image_file) ]

    elif os.path.isdir(source_dir):
        sorted_filenames = [filename for filename in sorted(os.listdir(source_dir)) if any(filename.lower().endswith(extension) for extension in supported_extensions) ]

        total_volume = len(sorted_filenames)

        if offset<0:        # support offsets "from the right"
            offset += total_volume

        volume = int(volume_str) if len(volume_str)>0 else total_volume-offset

        selected_filenames = sorted_filenames[offset:offset+volume]


    output_filenames = preprocess_files(
        selected_filenames, source_dir, destination_dir, crop_percentage, square_side, inter_size, convert_to_bgr, audit_test03,
        data_type, new_file_extension, normalize_data, subtract_mean, given_channel_means, interpolation_method)

    fof_full_path = os.path.join(destination_dir, fof_name)
    with open(fof_full_path, 'w') as fof:
        for filename in output_filenames:
            fof.write(filename + '\n')
