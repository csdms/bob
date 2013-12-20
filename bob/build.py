import os

from .bash_commands import TemplateScript


class EmptyBuilder(TemplateScript):
    _template = """
# Nothing to build
    """
    _hook = """
${build_hook}
    """
    def __init__(self, **kwds):
        kwds.setdefault('build_hook', '')
        super(EmptyBuilder, self).__init__(**kwds)


class AutotoolsBuilder(EmptyBuilder):
    """Build and install with autotools
    """
    _template = """
( mkdir -p ${build_dir} && \\
    cd ${build_dir} && \\
    ${src_dir}/configure --prefix=$PREFIX ${configure_flags} && \\
    make ${make_opts} all install ) || exit
"""
    def __init__(self, dir, **kwds):
        kwds.setdefault('configure_flags', '')
        kwds.setdefault('make_opts', '')
        kwds.setdefault('build_dir', os.path.join(dir, '_build'))
        kwds['src_dir'] = os.path.abspath(dir)

        super(AutotoolsBuilder, self).__init__(**kwds)


class MakeBuilder(TemplateScript):
    """Build and install with autotools
    """
    _template = """
( cd ${build_dir} && make ${make_opts} all ) || exit
"""
    def __init__(self, dir, **kwds):
        kwds.setdefault('make_opts', '')
        kwds['build_dir'] = os.path.abspath(dir)

        super(MakeBuilder, self).__init__(**kwds)


class CmakeBuilder(TemplateScript):
    """Build and install with CMake
    """
    _template = """
mkdir -p ${build_dir} && cd ${build_dir}
$cmake .. -DCMAKE_INSTALL_PREFIX=$PREFIX ${cmake_flags} && \\
    make ${make_opts} all install
"""
    def __init__(self, dir, **kwds):
        kwds.setdefault('configure_opts', '')
        kwds.setdefault('cmake_flags', '')
        kwds.setdefault('make_opts', '-j4')
        kwds['build_dir'] = os.path.join(dir, '_build')

        super(CmakeBuilder, self).__init__(**kwds)


class ContractorBuilder(TemplateScript):
    """Build and install with contractor
    """
    _template = """
( cd ${build_dir} && \\
        $python ./contract.py --configure prefix=$PREFIX cc=$cc cxx=$cc \\
            f77=$f77 python=$python java=$java babel_version=1.4.0 && \\
        ./contract.py ) || exit
"""
    def __init__(self, dir, **kwds):
        kwds['build_dir'] = os.path.abspath(dir)
        super(ContractorBuilder, self).__init__(**kwds)


