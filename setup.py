#!/usr/bin/env python
# Copyright (C) 2011 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from distutils.core import setup
from imagescaler.version import VERSION_STR

setup(
    name='imagescaler',
    description='Gamma-correct image scaler',
    license='GPL v2 or later',
    version=VERSION_STR,
    url='http://git.goodpoint.de/?p=imagescaler.git;a=summary',
    author='Sebastian Pipping',
    author_email='sebastian@pipping.org',
    packages=[
        'imagescaler',
        'imagescaler.algorithms',
    ],
    data_files=[
        ('/usr/lib/gimp/2.0/plug-ins/',
            ['gimpplugin/imagescalerplugin.py', ]),
    ],
)
