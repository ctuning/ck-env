#!/usr/bin/env python3

supported_extensions = ['jpeg', 'jpg', 'gif', 'png']

import os
import cv2


# Load and preprocess image
def load_image(image_path,            # Full path to processing image
               target_size,           # Desired size of resulting image
               intermediate_size = 0, # Scale to this size then crop to target size
               crop_percentage = 0,   # Crop to this percentage then scale to target size
               data_type = 'uint8',   # Data type to store
               convert_to_bgr = False # Swap image channel RGB -> BGR
               ):

    out_height  = target_size
    out_width   = target_size

    def resize_with_aspectratio(img, inter_pol=cv2.INTER_LINEAR):
        height, width, _ = img.shape
        new_height = int(100. * out_height / crop_percentage)   # intermediate oversized image from which to crop
        new_width = int(100. * out_width / crop_percentage)     # ---------------------- ,, ---------------------
        if height > width:
            w = new_width
            h = int(new_height * height / width)
        else:
            h = new_height
            w = int(new_width * width / height)

        img = cv2.resize(img, (w, h), interpolation = inter_pol)
        return img

    def center_crop(img):
        height, width, _ = img.shape
        left = int((width - out_width) / 2)
        right = int((width + out_width) / 2)
        top = int((height - out_height) / 2)
        bottom = int((height + out_height) / 2)
        img = img[top : bottom, left : right]
        return img


    img = cv2.imread(image_path)

    if len(img.shape) < 3 or img.shape[2] != 3:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Mimic Guenther Schuelling's preprocessing steps
    img = resize_with_aspectratio(img, cv2.INTER_AREA)
    img = center_crop(img)

    # Convert to BGR
    if convert_to_bgr:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    return img


def preprocess_files(selected_filenames, source_dir, destination_dir, crop_percentage, square_side, inter_size, convert_to_bgr, data_type, new_file_extension):
    "Go through the selected_filenames and preprocess all the files"

    output_filenames = []

    for current_idx in range(len(selected_filenames)):
        input_filename = selected_filenames[current_idx]

        full_input_path     = os.path.join(source_dir, input_filename)

        image_data = load_image(image_path = full_input_path,
                              target_size = square_side,
                              intermediate_size = inter_size,
                              crop_percentage = crop_percentage,
                              data_type = data_type,
                              convert_to_bgr = convert_to_bgr)

        output_filename = input_filename.rsplit('.', 1)[0] + '.' + new_file_extension if new_file_extension else input_filename

        full_output_path    = os.path.join(destination_dir, output_filename)
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
    convert_to_bgr          = os.getenv('_CONVERT_TO_BGR', '').lower() == 'yes'
    offset                  = int( os.getenv('_SUBSET_OFFSET', 0) )
    volume_str              = os.getenv('_SUBSET_VOLUME', '' )
    fof_name                = os.getenv('_SUBSET_FOF', 'fof.txt')
    data_type               = os.getenv('_DATA_TYPE', 'uint8')
    new_file_extension      = os.getenv('_NEW_EXTENSION', '')
    image_file              = os.getenv('CK_IMAGE_FILE', '')

    print("From: {} , To: {} , Size: {} , Crop: {} , InterSize: {} , 2BGR: {}, OFF: {}, VOL: '{}', FOF: {}, DTYPE: {}, EXT: {}, IMG: {}".format(
        source_dir, destination_dir, square_side, crop_percentage, inter_size, convert_to_bgr, offset, volume_str, fof_name, data_type, new_file_extension, image_file) )

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


    output_filenames = preprocess_files(selected_filenames, source_dir, destination_dir, crop_percentage, square_side, inter_size, convert_to_bgr, data_type, new_file_extension)

    fof_full_path = os.path.join(destination_dir, fof_name)
    with open(fof_full_path, 'w') as fof:
        for filename in output_filenames:
            fof.write(filename + '\n')
