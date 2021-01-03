# eulerangles
[![Build Status](https://travis-ci.com/alisterburt/eulerangles.svg?branch=master)](https://travis-ci.com/alisterburt/eulerangles)
[![Documentation Status](https://readthedocs.org/projects/eulerangles/badge/?version=latest)](https://eulerangles.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/eulerangles.svg)](https://pypi.org/project/eulerangles/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/eulerangles.svg)](https://pypi.python.org/pypi/eulerangles/)

# Quick Start
[Euler angles](https://en.wikipedia.org/wiki/Euler_angles) are often used to represent rigid body rotations in 3D. 

They can be defined in many different ways. The world of transformations is filled with 
[ambiguities](https://rock-learning.github.io/pytransform3d/transformation_ambiguities.html) which can make it harder 
than necessary to interface softwares which define their transformations differently.

`eulerangles` is designed to simplify the handling of large sets of 
Euler angles in Python.

## Features
- convert Euler angles into rotation matrices
- convert rotation matrices into Euler angles
- convert between differently defined Euler angles
- simple API
- vectorised implementation

## Documentation
Complete documentation is provided [here](https://eulerangles.readthedocs.io/en/latest/).
- [Quick Start](https://eulerangles.readthedocs.io/en/latest/usage/quick_start.html)
- [Installation](https://eulerangles.readthedocs.io/en/latest/usage/installation.html)
- [API Reference](https://eulerangles.readthedocs.io/en/latest/api.html)

## Installation
If you're already at ease with package management in Python, go ahead and 
```
pip install eulerangles
```

Otherwise, please see the 
[installation](https://eulerangles.readthedocs.io/en/latest/usage/installation.html) page.
