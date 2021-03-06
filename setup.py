#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search(
        "^__version__ = ['\"]([^'\"]+)['\"]$", init_py, re.MULTILINE
    ).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version('cli_bdd/')


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


setup(
    name='cli-bdd',
    version=version,
    url='https://github.com/chibisov/cli-bdd/',
    license='MIT',
    description='BDD for command-line applications',
    author='Gennady Chibisov',
    author_email='web-chib@ya.ru',
    install_requires=[
        'pyhamcrest>=1.8.5',
        'pexpect>=4.0.1'
    ],
    packages=get_packages('cli_bdd'),
    package_data=get_package_data('cli_bdd'),
)
