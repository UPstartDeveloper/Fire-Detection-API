# *The* Fire Detection API
![Project cover image](https://i.postimg.cc/1RNPLFF3/Screen-Shot-2021-09-02-at-9-58-41-AM.png)

Deep learning has the power to potentially save millions of dollars (and more importantly, lives) in places like California where the annual "fire season" arrives every Fall.

We built this API to show how the technology can fight this and other crises, and inspire our students to do the same.

## Getting Started

### Use the API
To classify your own images, you can use the live API: use the link [here](https://fire-detection-api.herokuapp.com/docs) to read the documentation and send requests.

### Running Locally
You can download this repository and run it using [Docker](https://www.docker.com/get-started):

```docker compose up```

Alternatively, you can also make a virtual environment and run it using the `uvicorn` package:

```
$ python3 -m venv env  # creates a virtualenv
$ source env/bin/activate  # now you're in the virtualenv
$ uvicorn app.main:app --reload  # run the app

```

## The Data and the Model
The image dataset and model used for the production API will be documented on the [Releases](https://github.com/UPstartDeveloper/Fire-Detection-API/releases) page of this repository.

## Making Your Own Deep Learning API

TBD

## Deploying to Heroku

TBD
## Stretch Challenges

In this project, we've worked with different tools like Tensorflow, Docker, FastAPI and Heroku. The next steps would be to two-fold:

- For the **modelling** engineers: how would you improve the neural networks performance?
- For the **MLOps** engineers: how would you improve the performance and scalability of the REST API in production?

## Credits and Resources
1. This *Towards Data Science* [blog](https://towardsdatascience.com/a-step-by-step-tutorial-to-build-and-deploy-an-image-classification-api-95fa449f0f6a) by Youness Mansar will give you a little more detail on how you can build a deployment-driven deep learning project (using the Google Cloud Platform's App Engine).
2. Another [blog](https://towardsdatascience.com/how-to-deploy-your-fastapi-app-on-heroku-for-free-8d4271a4ab9#beb1) by  Shinichi Okada in *Towards Data Science* will give more details how to deploy FastAPI applications (such as this repo!) on Heroku specifically.