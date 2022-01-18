"""
setup.py for the plant package.
"""
from os import path

import setuptools

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "requirements.txt")) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [
        line
        for line in requirements_file.read().splitlines()
        if not line.startswith("#")
    ]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Plant",
    version="0.0.1",
    author="Annalena Daniels & Samuel Tovey",
    author_email="tovey.samuel@gmail.com",
    description="Package for the monitoring of plants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/annalendaniels/Plant",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=requirements,
)
