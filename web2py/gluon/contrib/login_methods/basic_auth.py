from gluon._compat import urlopen
from gluon._compat import urllib2
import base64


def basic_auth(server="http://127.0.0.1"):
    """
    to use basic login with a different server
    from gluon.contrib.login_methods.basic_auth import basic_auth
    auth.settings.login_methods.append(basic_auth('http://server'))
    """

    def basic_login_aux(username,
                        password,
                        server=server):
        key_str = username + ':' + password
        key = base64.b64encode(key_str.encode("utf-8"))
        headers = {'Authorization': 'Basic ' + key_str}
        request = urllib2.Request(server, None, headers)
        try:
            urlopen(request)
            return True
        except (urllib2.URLError, urllib2.HTTPError):
            return False
    return basic_login_aux
