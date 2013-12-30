from __future__ import print_function

import os
import subprocess

from .build_environment import BuilderEnvironment
from .package_builder import PackageBuilder
from .package_cleaner import PackageCleaner
from .bash_commands import SheBang


def list(args):
    builder = PackageBuilder()
    builder.read('packages.cfg')
    sep = os.linesep

    print(sep.join(builder.packages))


def show(args):
    env = BuilderEnvironment()
    builder = PackageBuilder()
    builder.read('packages.cfg')

    print(SheBang('/bin/bash').tobash())
    print(env.tobash())
    if len(args.packages) > 0:
        for package in args.packages:
            print(builder.tobash(package))
    else:
        print(builder.tobash())


def build(args):
    env = BuilderEnvironment()
    builder = PackageBuilder()
    builder.read('packages.cfg')

    try:
        packages = args.package_file.read().split()
    except AttributeError:
        packages = []

    packages.extend(args.packages)

    lines = [SheBang('/bin/bash').tobash()]
    lines.append(env.tobash())
    if len(packages) > 0:
        for package in packages:
            lines.append(builder.tobash(package))
    else:
        lines.append(builder.tobash())

    script = os.linesep.join(lines)

    if args.run:
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(script), tmp.seek(0)
            subprocess.check_call(['/usr/bin/env', '-i', 'bash', tmp.name])
    else:
        print(script)


def clean(args):
    cleaner = PackageCleaner()
    cleaner.read('packages.cfg')

    lines = [SheBang('/bin/bash').tobash()]
    if len(args.packages) > 0:
        for package in args.packages:
            lines.append(cleaner.tobash(package))
    else:
        lines.append(cleaner.tobash())

    script = os.linesep.join(lines)

    if args.run:
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(script), tmp.seek(0)
            subprocess.check_call(['/usr/bin/env', '-i', 'bash', tmp.name])
    else:
        print(script)


def make_distribution_name(name, version=None):
    import os

    if version is not None:
        name = '-'.join([name, version])

    (sysname, nodename, release, version, machine) = os.uname()
    return '-'.join([name, sysname.lower(), machine])


def pack(args):
    import tarfile

    tar_file = '.'.join([make_distribution_name(args.name,
                                                version=args.version),
                         'tar.gz'])

    if os.path.isfile(tar_file) and not args.force:
        print('%s: file exists, not overwriting. use --force to overwrite.' %
              tar_file)
    else:
        with tarfile.open(tar_file, 'w:gz') as tar:
            tar.add(args.prefix)
