from .bash_commands import TemplateScript


class Cleaner(TemplateScript):
    """Clean up files
    """
    _template = """
rm -rf ${files}
    """
    def __init__(self, files, **kwds):
        kwds['files'] = ' '.join(files)
        super(Cleaner, self).__init__(**kwds)


