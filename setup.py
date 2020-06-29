from distutils.core import setup

from eulerangles import __version__

setup(
    name='eulerangles',
    packages=['eulerangles'],
    version=f'{__version__}',
    license='BSD 3-Clause License',
    description="Vectorised conversion between various possible euler angle conventions or generation of an associated "
                "set of rotation matrices. Supports conventions for various software packages used for single particle "
                "analysis and subtomogram averaging software.",
    author='Alister Burt',
    author_email='alisterburt@gmail.com',
    url='https://github.com/alisterburt/eulerangles',
    download_url=f'https://github.com/alisterburt/eulerangles/archive/v{__version__}.tar.gz',
    keywords=['transformation', 'euler angles', 'eulerian angles', 'cryo-EM', 'cryo-ET'],
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
