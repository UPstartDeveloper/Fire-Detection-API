from setuptools import setup
from setuptools import find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
        REQUIRED = f.read().split("\n")
except:
    REQUIRED = []

setup(
    name="YOUR_API_NAMME",
    version="0.1.0",
    description="ADD_A_DESCRIPTION",
    author="YOUR_NAME",
    author_email="YOUR_EMAIL",
    url="YOUR_REPO_URL",
    license="MIT",
    install_requires=REQUIRED,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=("example", "app", "data", "docker", "tests")),
)
