import os

from .read import packages_from_file
from .clean import Cleaner


class PackageCleaner(object):
    def __init__(self, packages={}):
        self._packages = packages

    def read(self, package_file):
        packages = packages_from_file(package_file)
        self._packages.update(packages)

    def tobash(self, *args):
        if len(args) == 0:
            args = self._packages.keys()

        script = []

        for package in args:
            files = self._packages[package]._options['clean'].split(os.linesep)
            cleaner = Cleaner(files)
            script.append(cleaner.tobash())

        return os.linesep.join(script)


