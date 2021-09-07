import unittest

from fastapi.testclient import TestClient
import tensorflow as tf

from app.main import app

client = TestClient(app)


class ClassifierAPITest(unittest.TestCase):

    TEST_COLOR_IMG_URL = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"

    def test_make_prediction_normal(self):
        """Client submits a RGB image and gets a valid response."""
        # A: get image
        image_path = tf.keras.utils.get_file(
            origin=self.TEST_COLOR_IMG_URL, cache_dir=".", cache_subdir="./test-assets"
        )
        with open(image_path, "rb") as f:
            # B: format a mock request
            files = {"file": (f.name, f, "multipart/form-data")}
            # C: make a request, and verify a valid prediction is returned
            response = client.post("/detect-fire", files=files)
            assert response.status_code == 307
