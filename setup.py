"""Pyshgp setup file."""
import os
from setuptools import setup, find_packages


exec(open("pyshgp/__init__.py").read())


def read(fname):
    """Read a file to a string."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyshgp",
    version=__version__,
    description="Push Genetic Programming in Python",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    keywords=["push gp", "genetic programming", "pushgp", "gp", "push"],
    author="Eddie Pantridge",
    author_email="erp12@hampshire.edu",
    license="LGPL",
    url="https://github.com/erp12/pyshgp",
    packages=find_packages(
        exclude=('examples', 'examples.*', 'tests', 'tests.*', 'docs', 'docs_source')
    ),
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
        "pandas>=0.23.4",
    ],
    setup_requires=[
        "pytest-runner",
        "flake8>=3.5.0",
        "flake8-docstrings>=1.3.0",
        "sphinx>=1.8.3",
        "m2r>=0.2.1",
        "mkdocs-nature>=0.3.1",
    ],
    tests_require=[
        "pytest"
    ],
)
