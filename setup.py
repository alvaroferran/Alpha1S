#!/usr/bin/env python


import setuptools


setuptools.setup(
    name="alpha1s",
    version="0.0.1",
    author="Alvaro Ferran",
    author_email="alvaroferran@gmail.com",
    description="Class to control Ubtech Alpha1S robot",
    url="https://github.com/alvaroferran/Alpha1S",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=['pybluez'],
    python_requires='>=3.6',
)
