import argparse

import numpy as np
import tensorflow as tf
from typing import Dict
import yaml

from classifier.util import preprocessing
from classifier.util.model import ModelUtility


class ImagePredictor:
    def __init__(self, config: Dict[str, int or str]):
        self.model_paths = config["model_file_paths"]
        self.resize_size = config["resize_shape"]
        self.model = ModelUtility.reconstruct_model(config)
        self.targets = config["targets"]

    @classmethod
    def init_from_config_path(cls, config_path):
        """Parses the config file, and instantiates a new ImagePredictor"""
        # load details for setting up the model
        with open(config_path, "r") as f:
            config = yaml.load(f, yaml.SafeLoader)
        # use the config data to integrate the model into the new instance
        predictor = cls(config)
        return predictor

    def predict_from_array(self, arr) -> Dict[str, float]:
        """Returns a prediction value the sample belongs to each class."""
        # in this model, 'Normal Images' is the positive class (labeled by 1)
        pred_arr = self.model.predict(arr[np.newaxis, ...]).ravel()
        pred = tf.keras.activations.sigmoid(pred_arr).numpy().tolist()
        # so we convert the probability to predict for 'Fire_Images'
        return {
            class_label: (1 - prob) for class_label, prob in zip(self.targets, pred)
        }

    def predict_from_file(self, file_object):
        """Converts uploaded image to a NumPy array and classifies it."""
        arr = preprocessing.read_from_file(file_object)
        return self.predict_from_array(arr)


if __name__ == "__main__":
    """
    Test out the predictor class via the CLI:
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
