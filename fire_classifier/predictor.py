import argparse

import numpy as np
from typing import List
import yaml
from tensorflow.keras.models import load_model

from fire_classifier.preprocessing_utilities import (
    read_img_from_path,
    read_from_file,
)
from fire_classifier.utils import download_model


class ImagePredictor:
    def __init__(
        self, model_paths: List[str], resize_size: List[int], targets: List[str]
    ):
        self.model_paths = model_paths
        self.model = load_model(self.model_paths)
        self.resize_size = resize_size
        self.targets = targets

    @classmethod
    def init_from_config_path(cls, config_path):
        with open(config_path, "r") as f:
            config = yaml.load(f, yaml.SafeLoader)
        predictor = cls(
            model_paths=config["model_paths"],
            resize_size=config["resize_shape"],
            targets=config["targets"],
        )
        return predictor

    @classmethod
    def init_from_config_url(cls, config_path):
        with open(config_path, "r") as f:
            config = yaml.load(f, yaml.SafeLoader)

        download_model(
            config["model_file_urls"], config["model_paths"], config["model_sha256"]
        )

        return cls.init_from_config_path(config_path)

    def predict_from_array(self, arr):
        pred = self.model.predict(arr[np.newaxis, ...]).ravel().tolist()
        pred = [round(x, 3) for x in pred]
        return {k: v for k, v in zip(self.targets, pred)}

    def predict_from_path(self, path):
        arr = read_img_from_path(path)
        return self.predict_from_array(arr)

    def predict_from_file(self, file_object):
        arr = read_from_file(file_object)
        return self.predict_from_array(arr)


if __name__ == "__main__":
    """
    python predictor.py --predictor_config "../example/predictor_config.yaml"

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--predictor_config_path",
        help="predictor_config_path",
        default="../example/predictor_config.yaml",
    )

    args = parser.parse_args()

    predictor_config_path = args.predictor_config_path

    predictor = ImagePredictor.init_from_config_path(predictor_config_path)
