# eulerangles
[![Build Status](https://travis-ci.com/alisterburt/eulerangles.svg?branch=master)](https://travis-ci.com/alisterburt/eulerangles)
[![Documentation Status](https://readthedocs.org/projects/eulerangles/badge/?version=latest)](https://eulerangles.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/eulerangles.svg)](https://pypi.org/project/eulerangles/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/eulerangles.svg)](https://pypi.python.org/pypi/eulerangles/)

[Euler angles](https://en.wikipedia.org/wiki/Euler_angles) are often used to represent rigid body rotations in 3D. 

These transformations can be defined in many different ways. The world of transformations is filled with 
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
Complete documentation is provided on [readthedocs.io](https://eulerangles.readthedocs.io/en/latest/).
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

## Overview
To keep usage simple, the package provides only five functions
- `euler2matrix`
- `matrix2euler`
- `euler2euler`
- `convert_eulers`
- `invert_rotation_matrices`

`euler2matrix` converts sets of Euler angles into rotation matrices.

`matrix2euler` converts sets of rotation matrices into Euler angles.

`euler2euler` converts between sets of Euler angles defined in different ways.

`convert_eulers` provides a simpler interface to `euler2euler`.

`invert_rotation_matrices` inverts sets of rotation matrices, yielding the inverse transformation.

## Examples
### `euler2matrix`

```python
import numpy as np
from eulerangles import euler2matrix

eulers = np.array([30, 60, 75])
rotation_matrix = euler2matrix(eulers,
                               axes='zyz',
                               intrinsic=True,
                               right_handed_rotation=True)
```
```python
>>> rotation_matrix
array([[-0.37089098, -0.54766767,  0.75      ],
       [ 0.90122107, -0.01733759,  0.4330127 ],
       [-0.22414387,  0.8365163 ,  0.5       ]])
```

multiple sets of Euler angles can be passed as an (n, 3) array-like object, 
in which case an (n, 3, 3) array of rotation matrices will be returned.

### `matrix2euler`
```python
import numpy as np
from eulerangles import matrix2euler

rotation_matrix = np.array([[-0.37089098, -0.54766767,  0.75      ],
                            [ 0.90122107, -0.01733759,  0.4330127 ],
                            [-0.22414387,  0.8365163 ,  0.5       ]])
eulers = matrix2euler(rotation_matrix,
                      axes='zyz',
                      intrinsic=True,
                      right_handed_rotation=True)
```

```python
>>> eulers
array([29.99999989, 60.        , 74.99999981])
```

multiple rotation matrices can be passed as an (n, 3, 3) array-like object, 
in which case an (n, 3) array of Euler angles will be returned.

### `euler2euler`
`euler2euler` is a verbose function for converting between sets of Euler angles defined differently.
- `source_` parameters relate to the input Euler angles
- `target_` parameters relate to the output Euler angles
- `invert_matrix` inverts the rotation matrix or matrices before generating output Euler angles

`invert_matrix` is useful when one set of Euler angles describe an active transformation, 
the other a passive transformation.

```python
import numpy as np
from eulerangles import euler2euler

input_eulers = np.array([-47.2730, 1.1777, -132.3000])
output_eulers = euler2euler(input_eulers,
                            source_axes='zxz',
                            source_intrinsic=True,
                            source_right_handed_rotation=True,
                            target_axes='zyz',
                            target_intrinsic=False,
                            target_right_handed_rotation=False,
                            invert_matrix=True)
```
```python
>>> output_eulers
array([ 42.727 ,  -1.1777, 137.7   ])
```

multiple sets of Euler angles can be passed as an (n, 3) array-like object, 
in which case an (n, 3) array of Euler angles will be returned.

### `convert_eulers`
`convert_eulers` provides a simpler interface to the verbose `euler2euler` function. 

Necessary metadata for conversion between input Euler angles and output Euler angles 
are stored in a `ConversionMeta` objects, defined as follows
```python
import numpy as np
from eulerangles import ConversionMeta, convert_eulers

source_metadata = ConversionMeta(name='input', 
                                axes='zyz', 
                                intrinsic=True, 
                                right_handed_rotation=True, 
                                active=True)

target_metadata = ConversionMeta(name='output', 
                                axes='zxz', 
                                intrinsic=False, 
                                right_handed_rotation=False, 
                                active=False)
```

these objects are used for conversion in `convert_eulers`

```python
input_eulers = np.array([10, 20, 30])
output_eulers = convert_eulers(input_eulers, 
                               source_meta=source_metadata, 
                               target_meta=target_metadata)
```
```python
>>> output_eulers
array([-80., -20., 120.])
```

For a select few software packages for 3D reconstruction from transmission electron microscopy images, 
`source_meta` and `target_meta` can be passed as a string corresponding to the name of the software package.

### `invert_rotation_matrices`
`invert_rotation_matrices` inverts rotation matrices such that they represent 
the inverse transform of the input rotation matrix.

Rotation matrices are orthogonal, therefore their inverse is simply the transpose.

```python
import numpy as np
from eulerangles import invert_rotation_matrices
rotation_matrix = np.array([[-0.37089098, -0.54766767,  0.75      ],
                            [ 0.90122107, -0.01733759,  0.4330127 ],
                            [-0.22414387,  0.8365163 ,  0.5       ]])

inverse_matrix = invert_rotation_matrices(rotation_matrix)
```

```python
>>> inverse_matrix
array([[-0.37089098,  0.90122107, -0.22414387],
       [-0.54766767, -0.01733759,  0.8365163 ],
       [ 0.75      ,  0.4330127 ,  0.5       ]])
```

This function works equally well on multiple rotation matrices passed as an (n, 3, 3) array.
