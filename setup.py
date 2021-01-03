from setuptools import setup, find_packages

from eulerangles.version import __version__

setup(
    name='eulerangles',
    packages=find_packages(include=['eulerangles', '*'], exclude=['test',]),
    version=f'{__version__}',
    license='BSD 3-Clause License',
    description="""Simplify the handling of large sets of Euler angles in Python
    """,
    author='Alister Burt',
    author_email='alisterburt@gmail.com',
    url='https://github.com/alisterburt/eulerangles',
    keywords=['transformation', 'euler angles', 'eulerian angles', 'cryo-EM', 'cryo-ET'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
