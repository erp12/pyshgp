# _*_ coding: utf_8 _*_
"""
Created on 9/1/2016

@author: Eddie
"""
import os
from setuptools import setup, find_packages


exec(open("pyshgp/__init__.py").read())


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyshgp",
    # version="0.1.0",
    version=__version__,
    description="Push Genetic Programming in Python",
    long_description=read('README.md'),
    keywords=["push gp", "genetic programming", "pushgp", "gp", "push"],
    author="Eddie Pantridge",
    author_email="erp12@hampshire.edu",
    license="LGPL",
    url="https://github.com/erp12/pyshgp",
    packages=find_packages(exclude=['examples', 'docs', 'tests*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        'Programming Language :: Python :: 3',
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    install_requires=[
        "numpy>=1.12.0",
        "scipy>=0.18.0",
        "scikit-learn>=0.18.0",
        "pandas>=0.23.4",
    ],
    setup_requires=[
        "pytest-runner",
        "flake8>=3.5.0",
        "flake8-docstrings>=1.3.0"
    ],
    tests_require=[
        "pytest"
    ],
)
