import hashlib
import os
from tensorflow import keras


def get_hash(filename):
    """
    Computes the SHA256 hash of a given file.

    This can then be used to ensure the model file(s) downloaded
    in this codebase are not corrupted.

    Args:
        filename(str): the name of the file

    Returns:
        bytes-like object
    """
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def download_model(url, file_paths, file_sha256=None):
    """
    Downloads the model files in memory.

    This will first check if the files are already present,
    and not corrupted, before downloading from the address
    specified in config.yaml.

    Args:
        url(str): the base url where the files are located
        file_paths(List[str]): collection of all the files needed to
                               eventually load the model
        file_sha256(str): the supposed hash of one of the files
                          we need to download. Checked against the
                          one we may already have in the codebase.

    Returns:
        None
    """
    # Download only the model files that are needed
    for model_file_path in file_paths:
        if os.path.exists(model_file_path):
            if get_hash(model_file_path) == file_sha256:
                print(f"File already exists: {model_file_path}")
        else:  # need to download the model
            model_file_url = f"{url}/{model_file_path}"
            keras.utils.get_file(
                origin=model_file_url,
                fname=model_file_path,
                cache_dir=".",
                cache_subdir="./model",
            )


def load_model(url, file_paths, file_sha256=None, format="composite"):
    """
    Model reconstruction.

    This will first load the model in memory using the given files
    and save format

    Args:
        url(str): the base url where the files are located
        file_paths(List[str]): collection of all the files needed to
                               eventually load the model
        file_sha256(str): the supposed hash of one of the files
                          we need to download. Checked against the
                          one we may already have in the codebase.
        format(str): currently this only supports 'composite'
                     (which is for when the model is saved using a H5 + JSON)
                     or 'h5' as the save format of the model.

    Returns:
        keras.Model object
    """

    def _model_from_composite_format():
        """Specific to using H5 + JSON as the save format"""
        params_file, layers_file = file_paths
        # load the model in memory
        with open(f"./model/{layers_file}") as f:
            model = keras.models.model_from_json(f.read())  # build the layers
            model.load_weights(f"./model/{params_file}")  # load weights + biases
        return model

    def _model_from_h5():
        """Specific to using a single Hadoop(H5) file"""
        params_file = file_paths[0]
        return keras.models.load_model(params_file)

    # First download the model, if needed
    download_model(url, file_paths, file_sha256)
    # load the model in memory
    if format == "composite":
        return _model_from_composite_format()
    else:  # assuming a single H5
        return _model_from_h5()
