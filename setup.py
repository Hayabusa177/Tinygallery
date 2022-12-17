#! /usr/bin/python3
from setuptools import *

setup(
    name = "tinyGallery",
    version = "1.0.0",
    package = "tinyGallery",
    include_package_data = True,
    install_requires=[
        "flask",
    ],
)