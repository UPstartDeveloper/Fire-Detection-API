from fastapi import FastAPI, File, UploadFile
from fire_classifier.predictor import ImagePredictor
from fire_classifier.util.api import API

# A: init API
app = FastAPI(title=API["title"], description=API["description"],
              version=API["version"], openapi_tags=API["endpoints"])

# B: init ML inference object, and the routes
predictor_config_path = API["config_path"]
predictor = ImagePredictor.init_from_config_path(predictor_config_path)


@app.post("/classify-image/", tags=["Detect Fire"])
def create_upload_file(file: UploadFile = File(...)):
    """Predicts the possibility that a RBG image contains fire."""
    return predictor.predict_from_file(file.file)
