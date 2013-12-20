from ConfigParser import SafeConfigParser

from .package_configure import PackageConfig


def packages_from_file(cfg_file):
    parser = SafeConfigParser()
    with open(cfg_file, 'r') as cfg:
        parser.readfp(cfg)

    packages = {}
    for package in parser.sections():
        packages[package] = PackageConfig(cfg_file, package)

    return packages


