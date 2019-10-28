#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

name = "pyVali"
here = path.abspath(path.dirname(__file__))

with open('./README.rst', encoding='utf-8') as f:
    long_description = f.read()
    long_description = long_description.replace("\r\n", "\n")

setup(
    name="pyVali",
    version="0.0.3",
    author="gpsbird",
    author_email="gpsbird@qq.com",
    description="python parameter validate",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/gpsbird/pyVali",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
