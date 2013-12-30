import os
from string import Template


class TemplateScript(object):
    _template = ''
    _hook = ''
    def __init__(self, **kwds):
        self._env = kwds

    def tobash(self, environ={}):
        script = Template(os.linesep.join([self._template.strip(),
                                           self._hook.strip()]))
        environ.update(self._env)
        return script.safe_substitute(environ)


class SheBang(object):
    """#! ${path}
    """
    def __init__(self, path):
        self._path = path

    def tobash(self):
        return '#! %s' % self._path


class Echo(object):
    """echo ${msg}
    """
    def __init__(self, msg):
        self._msg = msg

    def tobash(self):
        return 'echo %s' % self._msg


class ChangeDir(object):
    """cd ${dir}
    """
    def __init__(self, dir):
        self._dir = dir

    def tobash(self):
        return 'cd %s' % self._dir
