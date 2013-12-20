import os
from ConfigParser import SafeConfigParser
import warnings


class BuilderEnvironment(object):
    """Set up environment
    """
    required_options = set(['cmake', 'wget', 'pkg_config', 'tar', 'xz', 'svn'])

    def __init__(self, cfg_file='bob.cfg', environ={}):
        self._environ = environ
        self._environ.update(self.read(cfg_file))

    def warn_missing_options(self, opts):
        missing = self.required_options - set(opts)
        if len(missing) > 0:
            warnings.warn('%s: missing required option(s)' %
                          ', '.join(missing))

    def warn_unknown_options(self, opts):
        unknowns = set(opts) - self.required_options
        if len(unknowns) > 0:
            warnings.warn('%s: unrecognized option(s)' % ', '.join(unknowns))

    def read(self, cfg_file):
        parser = SafeConfigParser()
        parser.optionxform = str
        with open(cfg_file, 'r') as cfg:
            parser.readfp(cfg)

        prog_paths = {}

        try:
            paths = parser.items('bob')
        except NoSectionError:
            warnings.warn('%s: not a bob cfg file.' % cfg_file)
        else:
            self.warn_missing_options(parser.options('bob'))
            for prog in parser.options('bob'):
                try:
                    prog_paths[prog] = parser.get('bob', prog)
                except (NoSectionError, NoOptionError):
                    prog_paths[prog] = prog

        return prog_paths

    def tobash(self):
        lines = []
        for item in self._environ.items():
            lines.append('export %s="%s"' % item)
        lines.append('')
        return os.linesep.join(lines)
