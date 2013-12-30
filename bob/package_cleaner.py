import os

from .read import packages_from_file
from .clean import Cleaner
from .package_builder import BuildOrder


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

        clean_order = BuildOrder(*args, packages=self._packages)

        #for package in args:
        for package in clean_order.order:
            files = self._packages[package]._options['clean'].split(os.linesep)
            cleaner = Cleaner(files)
            script.append(cleaner.tobash())

        return os.linesep.join(script)


