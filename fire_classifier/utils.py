import hashlib
import os
from tensorflow import keras


def get_hash(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def download_model(urls, file_paths, file_sha256):
    params_file, layers_file = file_paths
    params_url, layers_url = urls
    if (
        os.path.exists(params_file)
        and os.path.exists(layers_file)
        and get_hash(layers_file) == file_sha256
    ):
        print("File already exists")
    else:
        keras.utils.get_file(
            origin=params_url, fname=params_file, cache_subdir=""
        )
        keras.utils.get_file(
            origin=layers_url, fname=layers_file, cache_subdir=""
        )
