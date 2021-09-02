import hashlib
import os
from tensorflow import keras


def get_hash(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def download_model(url, file_paths, file_sha256=None):
    params_file, layers_file = file_paths
    params_url, layers_url = (
        f"{url}/{params_file}",
        f"{url}/{layers_file}"
    )
    if (os.path.exists(params_file) and os.path.exists(layers_file)
        # and get_hash(layers_file) == file_sha256
    ):
        print("File already exists")
    else:  # download the model
        keras.utils.get_file(
            origin=layers_url, fname=layers_file,
            cache_dir='.', cache_subdir="./model"
        )
        keras.utils.get_file(
            origin=params_url, fname=params_file,
            cache_dir='.', cache_subdir="./model"
        )

def load_model(url, file_paths):
    '''Model reconstruction using H5 + JSON'''
    # First download the model, if needed
    download_model(url, file_paths)
    params_file, layers_file = file_paths
    # Model reconstruction
    with open(f"./model/{layers_file}") as f:
        model = keras.models.model_from_json(f.read())
        model.load_weights(f"./model/{params_file}")
    return model
