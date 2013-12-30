import os
from ConfigParser import SafeConfigParser

from .fetch import SvnFetcher, WgetFetcher
from .unpack import TarUnpacker, XzUnpacker
from .build import (CmakeBuilder, MakeBuilder, AutotoolsBuilder,
                    ContractorBuilder, EmptyBuilder)
from .install import InstallExecutable
from .build_script import BuildScript
from .bash_commands import Echo, ChangeDir


_FETCH_METHODS = {
    'svn': SvnFetcher,
    'wget': WgetFetcher,
}

_UNPACK_METHODS = {
    'tar': TarUnpacker,
    'xz': XzUnpacker,
}

_BUILD_METHODS = {
    'cmake': CmakeBuilder,
    'make': MakeBuilder,
    'autotools': AutotoolsBuilder,
    'contractor': ContractorBuilder,
}


class PackageConfig(object):
    def __init__(self, cfg_file, package):
        self._name = package
        self._file = cfg_file
        self._options = self._read_options()
        if 'requires' in self._options:
            import re
            requires = re.split('\s*[,\n]\s*', self._options['requires'])
            requires = [req for req in requires if len(req) > 0]
        else:
            requires = []
        self._requires = [base.strip() for base in requires]
        self._top_build_dir = os.getcwd()

    @property
    def name(self):
        return self._name

    @property
    def bases(self):
        return self._requires

    def tobash(self):
        to_top_dir = ChangeDir(self._top_build_dir)
        steps = [
            to_top_dir, self._construct_fetch_step(),
            to_top_dir, self._construct_unpack_step(),
            to_top_dir, self._construct_build_step(),
            to_top_dir, self._construct_install_step(),
        ]
        script = BuildScript(steps)
        return script.tobash()

    def _construct_fetch_step(self):
        fetch_from = self._options['fetch']

        try:
            method = self._options['fetch_method']
        except KeyError:
            if 'svn' in fetch_from:
                method = 'svn'
            else:
                method = 'wget'

        if method == 'svn':
            fetch = SvnFetcher(fetch_from, path=self._name, **self._options)
        elif method == 'wget':
            fetch = WgetFetcher(fetch_from)
        else:
            raise ValueError('%s: unknown fetch method' % method)

        return fetch

    def _construct_unpack_step(self):
        try:
            file = self._options['unpack']
        except KeyError:
            return Echo('nothing to unpack')

        try:
            method = self._options['unpack_method']
        except KeyError:
            if file.endswith('.tgz') or file.endswith('.tar.gz'):
                method = 'tar'
            elif file.endswith('.xz'):
                method = 'xz'
            else:
                raise ValueError('%s: no known unpacker' % unpack_file)

        try:
            unpack = _UNPACK_METHODS[method](file, **self._options)
        except KeyError:
            raise ValueError('%s: unknown unpack method' % method)

        return unpack

    def _construct_install_step(self):
        try:
            file = self._options['install']
        except KeyError:
            install = Echo('no install step')
        else:
            src_dir = self._options['build']
            install = InstallExecutable(os.path.join(src_dir, file),
                                        **self._options)
        return install

    def _construct_build_step(self):
        try:
            src_dir = self._options['build']
        except KeyError:
            return EmptyBuilder(**self._options)
            #return Echo('nothing to build')

        try:
            method = self._options['build_method']
        except KeyError:
            contents = os.listdir(src_dir)
            if 'CMakeLists.txt' in contents:
                method = 'cmake'
            elif 'configure' in contents:
                method = 'autotools'
            else:
                raise ValueError('%s: no known unpacker' % src_dir)
        
        try:
            build = _BUILD_METHODS[method](src_dir, **self._options)
        except KeyError:
            raise ValueError('%s: unknown build method' % method)

        return build

    def _get_fetch_method(self):
        try:
            method = self._options['fetch_method']
        except KeyError:
            fetch_from = self._options['fetch']
        fetch = _FETCH_METHODS[method]()

    def _read_options(self):
        parser = SafeConfigParser()
        with open(self._file, 'r') as cfg:
            parser.readfp(cfg)

        if not parser.has_section(self._name):
            raise

        return dict(parser.items(self._name))



