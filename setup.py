#!/usr/bin/env python

from distutils.core import setup

version = '0.1'

setup(
    name = 'webdriverwrapper',
    packages = [
        'webdriverwrapper',
    ],
    version = version,
    url = 'https://github.com/horejsek/python-webdriverwrapper',
    description = 'Better interface for WebDriver (Selenium 2).',
    author = 'Michal Horejsek',
    author_email = 'horejsekmichal@gmail.com',
    license = 'GNU General Public License (GPL)',
    classifiers = [
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        #'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)
