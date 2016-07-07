#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'futures>=3.0.5',
    'tornado>=4.3',
    'PyYAML>=3.11',
    'click>=6.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='blackgate',
    version='0.2.4',
    license='MIT',
    description="A set of utilities to build API gateway.",
    long_description=readme + '\n\n' + history,
    zip_safe=False,
    include_package_data=True,
    install_requires=requirements,
    platforms='any',
    author="Ju Lin",
    author_email='soasme@gmail.com',
    url='https://github.com/soasme/blackgate',
    packages=find_packages(exclude=('tests', 'tests.*', '*.tests', '*.tests.*', )),
    package_dir={'blackgate': 'blackgate'},
    keywords='microservices, api, gateway, server, production,',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'blackgate=blackgate.cli:main'
        ]
    },
)
