from __future__ import print_function

import os

from .read import packages_from_file


class BuildOrder(object):
    def __init__(self, *args, **kwds):
        self._packages = kwds.get('packages', {})
        if len(args) == 0:
            args = self._packages.keys()

        self._order = []
        for package in args:
            self._add(self._packages[package])

    @property
    def order(self):
        return self._order

    def _add(self, package):
        for base in package.bases:
            if base not in self._order:
                self._add(self._packages[base])
        if package.name not in self._order:
            self._order.append(package.name)

    def tobash(self):
        script = []
        for name in self._order:
            script.append(self._packages[name].tobash())
        return os.linesep.join(script)


class PackageBuilder(object):
    def __init__(self, packages={}):
        self._packages = packages

    @property
    def packages(self):
        return set(self._packages.keys())

    def read(self, package_file):
        packages = packages_from_file(package_file)
        self._packages.update(packages)

    def tobash(self, *args):
        script = []

        build_order = BuildOrder(*args, packages=self._packages)

        for package in build_order.order:
            script.append(self._packages[package].tobash())

        return os.linesep.join(script)


