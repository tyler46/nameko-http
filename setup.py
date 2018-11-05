#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()


setup(
    author="Spyros Markopoulos",
    author_email='virtualssuport@vermantia.com',
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Http utilities for Nameko built-in HTTP extension",
    install_requires=[
        'nameko>=2.11.0',
        'python-mimeparse>=1.6.0',
    ],
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nameko_http',
    name='nameko_http',
    packages=find_packages(include=['nameko_http']),
    extras_require={
        'dev': [
            'pip==18.1',
            'bumpversion==0.5.3',
            'wheel==0.32.2',
            'watchdog==0.9.0',
            'flake8==3.5.0',
            'pylint>=1.9.3',
            'tox==3.5.2',
            'coverage==4.5.1',
            'twine==1.12.1',
        ],
    },
    setup_requires=[
        'pytest-runner>=4.2',
    ],
    test_suite='tests',
    tests_require=[
        'pytest>=1.9.3',
        'requests-mock>=1.5.2',
    ],
    url='https://app.assembla.com/spaces/retail-platform/git-12/source',
    version='version='version='0.1.1''',
    zip_safe=False,
)
