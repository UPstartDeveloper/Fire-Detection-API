import hashlib
import os
from typing import Dict
from tensorflow import keras


class ModelUtility:
    def __init__(self, config: Dict[str, str]):
        """
        Instaniates a new object using data needed to load in the model.

        Args:
        config(dict): contains the following fields of interest:
            base_model_url(str): the base url where the files are located
            model_file_paths(list): collection of all the files needed to
                                         eventually load the model
            model_sha256(str): the supposed hash of one of the files
                               we need to download. Checked against the
                               one we may already have in the codebase.
        """
        self.url = config["base_model_url"]
        self.file_paths = config["model_file_paths"]
        self.file_sha256 = None
        if config["model_sha256"] is not None:
            self.file_sha256 = config["model_sha256"]

    @classmethod
    def reconstruct_model(cls, config):
        """Make a new instance, and load in the model straightaway."""
        model_utility = cls(config)
        # detect save format
        save_format = "composite"
        if config["model_file_paths"] and len(config["model_file_paths"]) == 1:
            save_format = "h5"
        # load the model
        return model_utility.load_model(save_format)

    def get_hash(self, filename):
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

    def download_model(self):
        """
        Downloads the model files in memory.

        This will first check if the files are already present,
        and not corrupted, before downloading from the address
        specified in config.yaml.

        Returns:
            None
        """
        # Download only the model files that are needed
        for model_file_path in self.file_paths:
            if os.path.exists(model_file_path):
                if self.get_hash(model_file_path) == self.file_sha256:
                    print(f"File already exists: {model_file_path}")
            else:  # need to download the model
                model_file_url = f"{self.url}/{model_file_path}"
                keras.utils.get_file(
                    origin=model_file_url,
                    fname=model_file_path,
                    cache_dir=".",
                    cache_subdir="./model",
                )

    def load_model(self, format="composite"):
        """
        Model reconstruction.

        This will first load the model in memory using the given files
        and save format

        Args:
            format(str): currently this only supports 'composite'
                        (which is for when the model is saved using a H5 + JSON)
                        or 'h5' as the save format of the model.

        Returns:
            keras.Model object
        """
        def _separate_files(file_paths):
            '''Looks for the H5 and/or JSON files in the given list.'''
            file1, file2 = file_paths
            # returns these file paths in the order: (some_file.h5, some_file.json)
            if file1.__contains__('.h5') or file1.__contains__('params'):
                return file1, file2
            else:  # the json file was listed first, so return the files in reverse
                return file2, file1

        def _model_from_composite_format():
            """Specific to using H5 + JSON as the save format"""
            params_file, layers_file = _separate_files(self.file_paths)
            # load the model in memory
            with open(f"./model/{layers_file}") as f:
                model = keras.models.model_from_json(f.read())  # build the layers
                model.load_weights(f"./model/{params_file}")  # load weights + biases
            return model

        def _model_from_h5():
            """Specific to using a single Hadoop(H5) file"""
            params_file = self.file_paths[0]
            return keras.models.load_model(params_file)

        # First download the model, if needed
        self.download_model()
        # load the model in memory
        if format == "composite":
            return _model_from_composite_format()
        else:  # assuming a single H5
            return _model_from_h5()
