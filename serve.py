import os, uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=os.getenv("HOST"), port=5000, log_level="info")