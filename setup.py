#!/usr/bin/env python

import os.path as op
from distutils.core import setup

from settingslib import __doc__, __version__, __author__, __email__


def read(fn):
    return open(op.join(op.dirname(__file__), fn), 'r').read()


setup(
    name='settingslib',
    version=__version__,
    author=__author__,
    author_email=__email__,
    license='New BSD',
    description=__doc__,
    long_description=read('README'),
    packages=['settingslib', ],
    url='http://github.com/kapishin/settingslib/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
    ],
)

