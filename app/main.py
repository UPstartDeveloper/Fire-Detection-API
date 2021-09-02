from fastapi import FastAPI, File, UploadFile
from fire_classifier.predictor import ImagePredictor

# init API
app = FastAPI(
    title="Fire Detection API",
    description="Informs the probability that an image contains fire.",
)

# init ML inference object
predictor_config_path = "./app/config.yaml"
predictor = ImagePredictor.init_from_config_path(predictor_config_path)


@app.post("/classify-image/")
def create_upload_file(file: UploadFile = File(...)):
    '''Predicts the possibility that a RBG image contains fire.'''
    return predictor.predict_from_file(file.file)
