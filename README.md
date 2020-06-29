# eulerangles
[![Build Status](https://travis-ci.com/alisterburt/eulerangles.svg?branch=master)](https://travis-ci.com/alisterburt/eulerangles)
[![PyPI version](https://badge.fury.io/py/eulerangles.svg)](https://pypi.org/project/eulerangles/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/eulerangles.svg)](https://pypi.python.org/pypi/eulerangles/)

`eulerangles` is a Python package to facilitate conversion between various possible conventions of [euler angles](https://en.wikipedia.org/wiki/Euler_angles)
describing rigid body transformations. It can also convert euler angles into rotation matrices and convert rotation matrices into euler angles.


## Features
- Supports all valid combinations of the x,y,z axes 
- supports intrinsic and extrinsic rotations
- Supports both positive CCW and positive CW rotation conventions (see conventions section)
- Predefined rotation conventions for some software packages used in single particle analysis and subtomogram averaging.
- Easy definition of custom rotation conventions
- Easy to install and use
- Vectorised with numpy for scalability



## Installation
Installation is available directly from the [Python package index](https://pypi.org/project/eulerangles/)
```
pip install eulerangles
```

## Conventions
### Angles
Angles should be given in degrees

### Axes
Three euler angles define sequential rotations 
<a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/gif.latex?R" title="R" /></a> by angles 
<a href="https://www.codecogs.com/eqnedit.php?latex=\alpha\beta\gamma" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\alpha\beta\gamma" title="\alpha\beta\gamma" /></a> 
about three principal axes with indices 
<a href="https://www.codecogs.com/eqnedit.php?latex=123" target="_blank"><img src="https://latex.codecogs.com/gif.latex?123" title="123" /></a>


<a href="https://www.codecogs.com/eqnedit.php?latex=\alpha\beta\gamma&space;\mapsto&space;R_{1}(\alpha)\rightarrow&space;R_{2}(\beta)\rightarrow&space;R_{3}(\gamma)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\alpha\beta\gamma&space;\mapsto&space;R_{1}(\alpha)\rightarrow&space;R_{2}(\beta)\rightarrow&space;R_{3}(\gamma)" title="\alpha\beta\gamma \mapsto R_{1}(\alpha)\rightarrow R_{2}(\beta)\rightarrow R_{3}(\gamma)" /></a>


### Rotation Matrices
All rotation matrices in this package are defined as (3,3) matrices which premultiply column vectors representing points



<a href="https://www.codecogs.com/eqnedit.php?latex=R&space;\begin{bmatrix}x&space;\\&space;y&space;\\&space;z&space;\end{bmatrix}&space;=&space;\begin{bmatrix}x'&space;\\&space;y'&space;\\&space;z'&space;\end{bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?R&space;\begin{bmatrix}x&space;\\&space;y&space;\\&space;z&space;\end{bmatrix}&space;=&space;\begin{bmatrix}x'&space;\\&space;y'&space;\\&space;z'&space;\end{bmatrix}" title="R \begin{bmatrix}x \\ y \\ z \end{bmatrix} = \begin{bmatrix}x' \\ y' \\ z' \end{bmatrix}" /></a>

Points are rotated about the origin.


### Intrinsic vs Extrinsic
- Intrinsic rotations are rotations that occur about the axes of a coordinate system attached to a moving body
- Extrinsic rotations are rotations that occur about the axes of a fixed coordinate system

In this intrinsic case they are defined as

<a href="https://www.codecogs.com/eqnedit.php?latex=R&space;=&space;R_1(\alpha)R_2(\beta)R_3(\gamma)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?R&space;=&space;R_1(\alpha)R_2(\beta)R_3(\gamma)" title="R = R_1(\alpha)R_2(\beta)R_3(\gamma)" /></a>

In the extrinsic case they are defined as

<a href="https://www.codecogs.com/eqnedit.php?latex=R&space;=&space;R_3(\gamma)R_2(\beta)R_1(\alpha)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?R&space;=&space;R_3(\gamma)R_2(\beta)R_1(\alpha)" title="R = R_3(\gamma)R_2(\beta)R_1(\alpha)" /></a>

### Direction of Rotation
`positive_ccw` in this package means that a positive angle will rotate a point counterclockwise about the given axis when looking from a positive point on that axis towards the origin.

This means that

<a href="https://www.codecogs.com/eqnedit.php?latex=R_z(90)\begin{bmatrix}1&space;\\&space;0&space;\\&space;0&space;\end{bmatrix}&space;=&space;\begin{bmatrix}0&space;\\&space;1&space;\\&space;0&space;\end{bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?R_z(90)\begin{bmatrix}1&space;\\&space;0&space;\\&space;0&space;\end{bmatrix}&space;=&space;\begin{bmatrix}0&space;\\&space;1&space;\\&space;0&space;\end{bmatrix}" title="R_z(90)\begin{bmatrix}1 \\ 0 \\ 0 \end{bmatrix} = \begin{bmatrix}0 \\ 1 \\ 0 \end{bmatrix}" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=R_y(90)\begin{bmatrix}0&space;\\&space;0&space;\\&space;1&space;\end{bmatrix}&space;=&space;\begin{bmatrix}1&space;\\&space;0&space;\\&space;0&space;\end{bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?R_y(90)\begin{bmatrix}0&space;\\&space;0&space;\\&space;1&space;\end{bmatrix}&space;=&space;\begin{bmatrix}1&space;\\&space;0&space;\\&space;0&space;\end{bmatrix}" title="R_y(90)\begin{bmatrix}0 \\ 0 \\ 1 \end{bmatrix} = \begin{bmatrix}1 \\ 0 \\ 0 \end{bmatrix}" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=R_x(90)\begin{bmatrix}0&space;\\&space;1&space;\\&space;0&space;\end{bmatrix}&space;=&space;\begin{bmatrix}0&space;\\&space;0&space;\\&space;1&space;\end{bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?R_x(90)\begin{bmatrix}0&space;\\&space;1&space;\\&space;0&space;\end{bmatrix}&space;=&space;\begin{bmatrix}0&space;\\&space;0&space;\\&space;1&space;\end{bmatrix}" title="R_x(90)\begin{bmatrix}0 \\ 1 \\ 0 \end{bmatrix} = \begin{bmatrix}0 \\ 0 \\ 1 \end{bmatrix}" /></a>


## Usage

### Creation of an EulerAngleConvention
#### General Case
```python
from eulerangles import EulerAngleConvention

convention = EulerAngleConvention(axes='ZXZ', intrinsic=True, positive_ccw=True)
other_convention = EulerAngleConvention(axes='XYZ', extrinsic=True, positive_ccw=False)
```

#### Single Particle Analysis and Subtomogram Averaging Conventions
For convenience, a specific object for dealing with conventions in single particle analysis and subtomogram averaging software packages is provided as `EMEulerAngleConvention` which adds a `reference frame` property describing 
whether the angles refer to rotations of a reference density map to align it with an experimental image or vice-versa as well as a `software` property containing the name of a given software package

```python
from eulerangles import EMEulerAngleConvention

convention = EMEulerAngleConvention(software='relion',
                                    axes='ZYZ',
                                    reference_frame='rotate_reference',
                                    positive_ccw=True,
                                    intrinsic=True),
```

### Conversion Between Different Euler Angle Conventions

```python
import numpy as np
from eulerangles import EulerAngleConvention, euler2euler

# Generate random euler angles
# Eulers should be an (n, 3) array-like object
input_shape = (50, 3)
input_eulers = np.random.randint(0, 180, input_shape)

# Define conventions for input and output euler angles
input_convention = EulerAngleConvention(axes='ZXZ', intrinsic=True, positive_ccw=True)
output_convention = EulerAngleConvention(axes='XYZ', extrinsic=True, positive_ccw=False)

# Convert eulers from input convention to output convention
output_eulers = euler2euler(input_eulers, source_convention=input_convention, target_convention=output_convention)
```

```
>>> input_eulers[0:5, :]
array([[144, 172, 122],
       [ 47,  60, 106],
       [166,  13,   4],
       [ 94,  88,  67],
       [ 51, 161,  66]])

>>> output_eulers[0:5, :]
array([[ 175.74074302,    6.77816127,   -7.29217251],
       [  25.52064487,   56.35403798, -122.94567298],
       [ -12.96940458,    0.89911037, -179.08673309],
       [ -84.89287959,   66.91791209,  -93.68838985],
       [-172.02754296,   17.30278659,  -17.78403893]])
```

For already implemented euler angle conventions (RELION, Dynamo, emClarity, WARP, M, PEET) you can provide the name of 
the software package directly rather than providing an `EulerAngleConvention` object. 

```python
output_eulers = euler2euler(input_eulers, source_convention='Dynamo', target_convention='M')
```
Names are not case sensitive.

### Deriving Rotation Matrices
A function `euler2matrix` is provided which allows conversion between euler angles and rotation matrices.

```python
from eulerangles import euler2matrix, EulerAngleConvention

# Define some euler angles
eulers = [[32, 124.5, 18],
          [88, 14, 116]]

# Convert euler angles to rotation matrices
rotation_matrices = euler2matrix(eulers, axes='ZXZ', extrinsic=True, positive_ccw=False)
```

Output is an (n, 3, 3) array of rotation matrices where n is the number of sets of euler angles provided
```
>>> rotation_matrices.shape
(2, 3, 3)
```

### Calculating Euler Angles from Rotation Matrices
Rotation matrices can also be converted into euler angles with the `matrix2euler` function

```python
from eulerangles import matrix2euler
eulers = matrix2euler(rotation_matrices, target_axes='ZXZ', target_positive_ccw=True, target_intrinsic=True)
```

```
>>> eulers
array([[162. , 124.5, 148. ],
       [ 64. ,  14. ,  92. ]])
```

## License
The project is released under the BSD 3-Clause License

## Known Issues
- Tested conventions are Dynamo, RELION, Warp, M - other conventions are taken from the websites of each software package