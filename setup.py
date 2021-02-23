from __future__ import print_function

import sys

if sys.version_info < (3, 6):
    print("Required python3 version >= 3.6", file=sys.stderr)
    sys.exit(1)

import io
import os
from setuptools import setup

packages = []

install_requires = []

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.md")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

version = "1.12.8"

setup(
    name="plea-punch",
    version=version,
    description="Plea Punch is a debate game",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Fabricio R Reinert",
    author_email="googleapis-packages@google.com",
    url="https://github.com/frreinert/plea-punch",
    install_requires=install_requires,
    python_requires=">=3.6",
    packages=packages,
    package_data={},
    license="MIT License",
    keywords="python debate game",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)