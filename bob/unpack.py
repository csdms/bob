import os

from .bash_commands import TemplateScript


class TarUnpacker(TemplateScript):
    """Unpack tar file
    """

    _template = """
$tar xvfz ${tar_file}
"""

    _hook = """
${unpack_hook}
    """

    def __init__(self, file, **kwds):
        kwds['tar_file'] = file
        kwds.setdefault('unpack_hook', '')
        super(TarUnpacker, self).__init__(**kwds)


class XzUnpacker(TemplateScript):
    """Unpack an xz file
    """

    _template = """
$xz --decompress ${xz_file}
$tar xvf ${tar_file}
"""

    def __init__(self, file, **kwds):
        (tar_file, _) = os.path.splitext(file)
        kwds['xz_file'] = file
        kwds['tar_file'] = tar_file
        super(XzUnpacker, self).__init__(**kwds)


