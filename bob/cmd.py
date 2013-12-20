#! /usr/bin/env python

from __future__ import absolute_import

from .subcommands import list, show, build, clean, pack


def main():
    import argparse

    parser = argparse.ArgumentParser('Let Bob do the building')
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser('list', help='list known packages')
    list_parser.set_defaults(func=list)

    show_parser = subparsers.add_parser('show', help='show build scripts')
    show_parser.add_argument('packages', nargs='*', help='packages to build')
    show_parser.set_defaults(func=show)

    build_parser = subparsers.add_parser('build', help='build packages')
    build_parser.add_argument('packages', nargs='*', help='packages to build')
    build_parser.add_argument('--run', default=False, action='store_true',
                              help='packages to build')
    build_parser.set_defaults(func=build)

    clean_parser = subparsers.add_parser('clean', help='clean build files')
    clean_parser.add_argument('packages', nargs='*', help='packages to build')
    clean_parser.add_argument('--run', default=False, action='store_true',
                              help='packages to build')
    clean_parser.set_defaults(func=clean)

    pack_parser = subparsers.add_parser('pack', help='pack up a distribution')
    pack_parser.add_argument('--force', default=False, action='store_true',
                             help='overwrite existing files')
    pack_parser.set_defaults(func=pack)

    args = parser.parse_args()

    args.func(args)
