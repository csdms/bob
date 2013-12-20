from .bash_commands import TemplateScript


class SvnFetcher(TemplateScript):
    """Checkout from repository
    """
    _template = """
$svn checkout ${repo}@${rev} ${path}
${fetch_hook}
"""
    def __init__(self, repo, **kwds):
        kwds.setdefault('rev', 'HEAD')
        kwds.setdefault('path', '')
        kwds['repo'] = repo
        kwds.setdefault('fetch_hook', '')
        super(SvnFetcher, self).__init__(**kwds)


class WgetFetcher(TemplateScript):
    """Grab a file from the web
    """
    _template = """
$wget ${url}
"""
    def __init__(self, url, **kwds):
        kwds['url'] = url
        super(WgetFetcher, self).__init__(**kwds)
