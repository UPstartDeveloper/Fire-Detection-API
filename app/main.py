from fastapi import FastAPI, File, UploadFile
from fire_classifier.predictor import ImagePredictor

# A: define description for the API endpoints (shown on UI)
endpoint_metadata = [
    {
        "name": "classify-image",
        "description": "Predicts the possibility that a RBG image contains fire.",
    },
]
# B: init API
app = FastAPI(
    title="DeepFire",
    description="A REST API for detecting the presence of fire in an image.",
    version="0.0.2",
    openapi_tags=endpoint_metadata,
)

# C: init ML inference object
predictor_config_path = "./app/config.yaml"
predictor = ImagePredictor.init_from_config_path(predictor_config_path)


@app.post("/classify-image/", tags=["classify-image"])
def create_upload_file(file: UploadFile = File(...)):
    """Predicts the possibility that a RBG image contains fire."""
    return predictor.predict_from_file(file.file)
