from fastapi import FastAPI, File, UploadFile
from classifier.predictor import ImagePredictor
from app.settings import API_SETTINGS

# A: init API
app = FastAPI(
    title=API_SETTINGS["title"],
    description=API_SETTINGS["description"],
    version=API_SETTINGS["version"],
    openapi_tags=API_SETTINGS["openapi_tags"],
)

# B: init ML inference object, and the routes
predictor_config_path = API_SETTINGS["predictor_config_path"]
predictor = ImagePredictor.init_from_config_path(predictor_config_path)


@app.post("/detect-fire/", tags=["Detect Fire in an Image"])
def make_prediction(file: UploadFile = File(...)):
    """Predicts the possibility that a RBG image contains fire."""
    return predictor.predict_from_file(file.file)
