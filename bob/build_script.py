import os

class BuildScript(object):
    """Build package
    """
    def __init__(self, steps=[]):
        self._steps = steps

    def tobash(self):
        script = []
        for step in self._steps:
            try:
                comment = '# %s' % step.__doc__.strip()
            except AttributeError:
                comment = ''
            finally:
                script.extend([comment, step.tobash(), ''])

        return os.linesep.join(script)


