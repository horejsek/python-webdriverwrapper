#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from pip.req import parse_requirements

version = '1.1.0'

setup(
    name='webdriverwrapper',
    version=version,
    packages=['webdriverwrapper'],

    install_requires=[str(ir.req) for ir in parse_requirements('requirements.txt')],

    url='https://github.com/horejsek/python-webdriverwrapper',
    author='Michal Horejsek',
    author_email='horejsekmichal@gmail.com',
    description='Better interface for WebDriver (Selenium 2).',
    license='PSF',

    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)
