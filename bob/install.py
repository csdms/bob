class InstallExecutable(TemplateScript):
    """Install a file.
    """
    _template = """
install ${install_flags} ${file} $PREFIX/bin || exit
    """
    def __init__(self, file, **kwds):
        kwds.setdefault('install_flags', '')
        kwds['file'] = file
        super(InstallExecutable, self).__init__(**kwds)


