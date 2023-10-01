#!/usr/bin/env python

"""The setup script."""

from pathlib import Path
from setuptools import setup, find_packages

pkg_path = Path(__file__).absolute().parent

with open(pkg_path / "requirements.txt") as f:
    requirements = f.readlines()

test_requirements = []

setup(
    author="M Salvaris",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    description="A quick and easy image gallery",
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "image-server=image_server.server:main",
        ]
    },
    name="image-server",
    packages=find_packages(include=["image_server", "image_server.*"]),
    url="https://github.com/msalvaris/image-server",
    version="0.0.1",
    zip_safe=False,
)
