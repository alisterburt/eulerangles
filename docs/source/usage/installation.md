# Installation
`eulerangles` is available through [PyPI](https://pypi.org/project/eulerangles/).

The latest version of the package can be installed with `pip`

```
pip install eulerangles
```

## Dependencies
`eulerangles` depends on [Numpy](https://numpy.org/) for fast, vectorised mathematical operations.

## A note about virtual environments
One Python installation may not be able to simultaneously meet the requirements of many interdependent packages,
some of which may require newer and older versions of the same package.

To get around this issue, it is recommended to work within virtual environments. 
Virtual environments provide an isolated Python installation with a set of required packages for a given project, 
environments can be activated and deactivated at will.

Virtual environments can be managed with
[venv](https://docs.python.org/3/tutorial/venv.html)
or
[conda](https://docs.conda.io/en/latest/).

A complete conda installation containing many packages for data science is provided by 
[Anaconda](https://www.anaconda.com/products/individual). 
A lightweight version [Miniconda](https://docs.conda.io/en/latest/miniconda.html) is also available.

The author of this package uses `conda` (via Miniconda) to manage software environments.
