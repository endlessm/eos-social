from BaseHTTPServer import BaseHTTPRequestHandler
import sys
import urlparse
import urllib
import urllib2
#from facebook import get_access_token_from_code, GraphAPIError

class FBHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def __init__(self, presenter, *args):
        self._presenter = presenter
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        code = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('code')
        code = code[0] if code else None
        if code is None:
            self.wfile.write("Sorry, authentication failed.")
            self._presenter.close_fb_auth_view()
            sys.exit(1)
        response = self.get('/oauth/access_token', {'client_id':self._presenter._app_id,
                                               'redirect_uri':self._presenter._webserver_url,
                                               'client_secret':self._presenter._app_secret,
                                               'code':code})
        self._presenter._fb_access_token = urlparse.parse_qs(response)['access_token'][0]
        open(self._presenter._model.LOCAL_FACEBOOK_FILE,'w').write(self._presenter._fb_access_token)
        self.wfile.write("You have successfully logged in to facebook. "
                         "You can close this window now.")
        self._presenter.close_fb_auth_view()
    
    def get_url(self, path, args=None):
        args = args or {}
        if self._presenter._fb_access_token:
            args['access_token'] = self._presenter._fb_access_token
        if 'access_token' in args or 'client_secret' in args:
            endpoint = "https://"+self._presenter._fb_graph_url
        else:
            endpoint = "http://"+self._presenter._fb_graph_url
        return endpoint+path+'?'+urllib.urlencode(args)

    def get(self, path, args=None):
        return urllib2.urlopen(self.get_url(path, args=args)).read()