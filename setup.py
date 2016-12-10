# _*_ coding: utf_8 _*_
"""
Created on 9/1/2016

@author: Eddie
"""
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "pysh_gp",
    version = "1.0.0",
    author = "Eddie Pantridge",
    author_email = "erp12@hampshire.edu",
    description = "Push Genetic Programming in Python",
    license = "LGPL",
    keywords = ["push gp", "genetic programming", "pushGP", "gp", "push"],
    url = "https://github.com/erp12/Pysh",
    packages=['pysh', 'pysh.gp', 'pysh.instructions'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Machine Learning",
        "Topic :: Genetic Programming",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    ],
)