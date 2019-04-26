#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='webdriverwrapper',
    version='2.8.0',  # Can't use VERSION because of imports during install before installing dependencies.
    packages=[
        'webdriverwrapper',
        'webdriverwrapper.pytest',
        'webdriverwrapper.unittest',
    ],

    install_requires=[
        'requests',
        'selenium',
    ],
    extras_require={
        'suggestion': [
            'python-Levenshtein',
        ],
        'devel': [
            'pylint',
            'pytest',
            'pyvirtualdisplay',
        ],
    },

    url='https://github.com/horejsek/python-webdriverwrapper',
    author='Michal Horejsek',
    author_email='horejsekmichal@gmail.com',
    description='Better interface for WebDriver (Selenium 2).',
    license='PSF',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)
