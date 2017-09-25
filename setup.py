#!/usr/bin/env python3

from setuptools import setup, find_packages

requirements = [
    'pulpcore-plugin',
]

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='pulp-example',
    version='0.0.1a1',
    description='Example plugin for the Pulp Project',
    long_description=long_description,
    author='Pulp Project Developers',
    author_email='pulp-dev@redhat.com',
    url='http://www.pulpproject.org/',
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(exclude=['test']),
    entry_points={
        'pulpcore.plugin': [
            'pulp_example = pulp_example:default_app_config',
        ]
    }
)
