#!/usr/bin/env python3

supported_extensions = ['jpeg', 'jpg', 'gif', 'png']

import os
import tensorflow as tf
from preprocessing import vgg_preprocessing as prep

tf.enable_eager_execution()     # execute commands immediately, instead of creating a graph and waiting for sess.run()

# Load and preprocess image
def load_image(image_path,            # Full path to processing image
               target_size            # Desired size of resulting image
               ):

    image_raw     = tf.read_file(image_path)
    image_tensor  = tf.image.decode_image(image_raw)

    if image_tensor.get_shape()[2]==1:
        image_tensor = tf.image.grayscale_to_rgb( image_tensor )

    preprocessed_float_numpy  = prep.preprocess_image(image_tensor, target_size, target_size).numpy()

    return preprocessed_float_numpy


def preprocess_files(selected_filenames, source_dir, destination_dir, square_side, data_type, new_file_extension):
    "Go through the selected_filenames and preprocess all the files"

    output_filenames = []

    for current_idx in range(len(selected_filenames)):
        input_filename = selected_filenames[current_idx]

        full_input_path     = os.path.join(source_dir, input_filename)

        image_data = load_image(image_path = full_input_path,
                              target_size = square_side)

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
    offset                  = int( os.getenv('_SUBSET_OFFSET', 0) )
    volume_str              = os.getenv('_SUBSET_VOLUME', '' )
    fof_name                = os.getenv('_SUBSET_FOF', 'fof.txt')
    data_type               = os.getenv('_DATA_TYPE', 'uint8')
    new_file_extension      = os.getenv('_NEW_EXTENSION', '')
    image_file              = os.getenv('CK_IMAGE_FILE', '')

    print("From: {} , To: {} , Size: {} , OFF: {}, VOL: '{}', FOF: {}, DTYPE: {}, EXT: {}, IMG: {}".format(
        source_dir, destination_dir, square_side, offset, volume_str, fof_name, data_type, new_file_extension, image_file) )

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


    output_filenames = preprocess_files(selected_filenames, source_dir, destination_dir, square_side, data_type, new_file_extension)

    fof_full_path = os.path.join(destination_dir, fof_name)
    with open(fof_full_path, 'w') as fof:
        for filename in output_filenames:
            fof.write(filename + '\n')
