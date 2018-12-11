import os
import skimage


def get_file_names_in_(folder, undesired_format):
    _file_names = []
    for _file_name in os.listdir(folder):
        if undesired_format not in _file_name:
            _file_names.append(os.path.join(folder, _file_name))
    return _file_names


def read_image_files_from_(_file_names):
    _image_files = []
    for _file_name in _file_names:
        _image_files.append(skimage.io.imread(_file_name))
    return _image_files


def write_image_files_from_(_file_names, _image_files):
    for i, _ in enumerate(_file_names):
        skimage.io.imsave(_file_names[i], _image_files[i])


def get_modified_file_names_in_():
    _modified_file_names = []
    for file_name in file_names:
        _modified_file_names.append(file_name.replace(DATA_FOLDER_LOCATION, EMPTY_STRING))
    return _modified_file_names


def modify_image_files(_image_files):
    _modified_image_files = []
    for _image_file in _image_files:
        _modified_image_files.append(
            skimage.transform.rescale(_image_file, SCALING_FACTOR, anti_aliasing=SCALING_ANTI_ALIASING, multichannel=SCALING_MULTICHANNEL, mode=SCALING_MODE))
    return _modified_image_files


UNDESIRED_FILE_FORMAT = '.DS_Store'
DATA_FOLDER = 'raw'
EMPTY_STRING = ''
DATA_FOLDER_LOCATION = '/'+DATA_FOLDER
SCALING_FACTOR = 4
SCALING_ANTI_ALIASING = False  # TODO is this default =-) or =-(
SCALING_MULTICHANNEL = False  # TODO is this default =-) or =-(
SCALING_MODE = 'constant' # TODO is this default =-) or =-(

cwd = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.join(cwd, DATA_FOLDER)
file_names = get_file_names_in_(data_folder, UNDESIRED_FILE_FORMAT)
image_files = read_image_files_from_(file_names)
modified_file_names = get_modified_file_names_in_()
modified_image_files = modify_image_files(image_files)
write_image_files_from_(modified_file_names, modified_image_files)
