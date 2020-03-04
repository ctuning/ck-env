#!/usr/bin/env python3

supported_extensions = ['jpeg', 'jpg', 'gif', 'png']

import errno
import os
import json

import numpy as np
import cv2


# Load and preprocess image
def load_image(image_path,            # Full path to processing image
               target_size,           # Desired size of resulting image
               data_type              # Data type to store
               ):

    image = cv2.imread(image_path)

    if len(image.shape) < 3 or image.shape[2] != 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    original_height, original_width, _ = image.shape
    
#    image_id = ck_utils.filename_to_id(image_file, DATASET_TYPE)
#    processed_image_ids.append(image_id)

    # The array based representation of the image will be used later 
    # in order to prepare the result image with boxes and labels on it.

    image = cv2.resize(image, (target_size, target_size), interpolation=cv2.INTER_LINEAR)

    # Conver to NumPy array
    img_data = np.asarray(image, dtype=data_type)

    # Make batch from single image
    batch_shape = (1, target_size, target_size, 3)
    batch_data = img_data.reshape(batch_shape)

    return batch_data, original_width, original_height


def preprocess_files(selected_filenames, source_dir, destination_dir, square_side, data_type, new_file_extension):
    "Go through the selected_filenames and preprocess all the files"

    output_signatures = []

    for current_idx in range(len(selected_filenames)):
        input_filename = selected_filenames[current_idx]

        full_input_path     = os.path.join(source_dir, input_filename)

        image_data, original_width, original_height = load_image(image_path = full_input_path,
                                                                target_size = square_side,
                                                                data_type = data_type)

        output_filename = input_filename.rsplit('.', 1)[0] + '.' + new_file_extension if new_file_extension else input_filename

        full_output_path    = os.path.join(destination_dir, output_filename)
        image_data.tofile(full_output_path)

        print("[{}]:  Stored {}".format(current_idx+1, full_output_path) )

        output_signatures.append('{};{};{}'.format(output_filename, original_width, original_height) )

    return output_signatures


if __name__ == '__main__':
    import sys

    source_dir              = sys.argv[1]   # ignored if CK_IMAGE_FILE points to a file
    destination_dir         = sys.argv[2]

    square_side             = int( os.environ['_INPUT_SQUARE_SIDE'] )
    offset                  = int( os.getenv('_SUBSET_OFFSET', 0) )
    volume_str              = os.getenv('_SUBSET_VOLUME', '' )
    fof_name                = os.getenv('_SUBSET_FOF', 'fof.txt')
    data_type               = os.getenv('_DATA_TYPE', 'uint8')
    new_file_extension      = os.getenv('_NEW_EXTENSION', '')
    image_file              = os.getenv('CK_IMAGE_FILE', '')

    print("From: {} , To: {} , Size: {} ,  OFF: {}, VOL: '{}', FOF: {}, DTYPE: {}, EXT: {}, IMG: {}".format(
        source_dir, destination_dir, square_side, offset, volume_str, fof_name, data_type, new_file_extension, image_file) )

    if image_file:
        source_dir          = os.path.dirname(image_file)
        selected_filenames  = [ os.path.basename(image_file) ]

    else:
        annotations_filepath = os.getenv('CK_ENV_DATASET_ANNOTATIONS')

        if annotations_filepath:            # get the "coco-natural" filename order (not necessarily alphabetic)
            with open(annotations_filepath, "r") as annotations_fh:
                annotations_struct = json.load(annotations_fh)

            ordered_filenames = [ image_entry['file_name'] for image_entry in annotations_struct['images'] ]

        elif os.path.isdir(source_dir):     # in the absence of "coco-natural", use alphabetic order

            ordered_filenames = [filename for filename in sorted(os.listdir(source_dir)) if any(filename.lower().endswith(extension) for extension in supported_extensions) ]

        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), source_dir)

        total_volume = len(ordered_filenames)

        if offset<0:        # support offsets "from the right"
            offset += total_volume

        volume = int(volume_str) if len(volume_str)>0 else total_volume-offset

        selected_filenames = ordered_filenames[offset:offset+volume]


    output_signatures = preprocess_files(selected_filenames, source_dir, destination_dir, square_side, data_type, new_file_extension)

    fof_full_path = os.path.join(destination_dir, fof_name)
    with open(fof_full_path, 'w') as fof:
        for filename in output_signatures:
            fof.write(filename + '\n')
