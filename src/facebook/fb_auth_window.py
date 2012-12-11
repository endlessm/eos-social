import gtk
import gobject
import webkit
import urllib
import urllib2
import urlparse

class FBAuthWindow(gtk.Window):
    def __init__(self, presenter=None, url='', width=800, height=600):
        print 'Initializing TestWindow...'
        super(FBAuthWindow, self).__init__()
        self._presenter = presenter
        self._authorized = False
        self.scroller = gtk.ScrolledWindow()
        self.web_view = webkit.WebView()
        self.web_view.connect("navigation-requested", self.on_navigation_requested)
        self.web_view.open('http://graph.facebook.com/oauth/authorize?scope=read_stream%2Cpublish_stream&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&client_id=393860344022808')
        self.web_view.show()
#        print 'Done...'
#        print 'Showing window...'
        self.scroller.add(self.web_view)
        self.scroller.show()
        self.add(self.scroller)
        self.set_size_request(width, height)
#        self.set_position(gtk.WIN_POS_CENTER)
        self.show()
        self.connect("delete-event", self.on_destroy)
#        print 'Done.'
    
    def on_navigation_requested(self, view, frame, request, data=None):
#        print 'Navigation requested...'
        uri = request.get_uri()
        parsed = urlparse.urlparse(uri)
#        print 'SCHEME:', parsed.scheme
#        print 'PATH  :', parsed.path
#        print 'QUERY :', parsed.query
#        print 'PARAMS:', parsed.params
        parsed_query = urlparse.parse_qs(parsed.query)
#        print parsed_query
        # ukoliko imam code onda idem po access token i cuvam ga
        if parsed_query.has_key('code'):
            # isto sto i u request handleru
            code = parsed_query['code'][0]
            token = self.get_access_token(code)
            if token:
#                self._presenter.set_fb_access_token(token)
                print 'ACCESS_TOKEN:' + token
                self._authorized = True
            self.emit("delete-event", gtk.gdk.Event(gtk.gdk.DELETE))
            
#            path = '/oauth/access_token'
#            params = {'client_id':self._presenter._app_id,
#                      'redirect_uri':self._presenter._webserver_url,
#                      'client_secret':self._presenter._app_secret,
#                      'code':code}
#            response = self.get(path, params)
#            token = urlparse.parse_qs(response)['access_token'][0]
            
#            self._authorized = True
            
        elif parsed_query.has_key('error'):
            print 'ERROR occured.'
            self.emit("delete-event", gtk.gdk.Event(gtk.gdk.DELETE))
        # ukoliko imam error_reason=user_denied ... sta da radim???
        return False
    
    def get_access_token(self, code):
        url = 'https://graph.facebook.com/oauth/access_token'
        params = {'client_id':'393860344022808',
                  'redirect_uri':'http://localhost:8080/',
                  'client_secret':'eb0dcb05f7512be39f7a3826ce99dfcd',
                  'code':code}
        url = url + '?' + urllib.urlencode(params)
#        print 'URL  :', url
        try:
            response = urllib2.urlopen(url).read()
#            print response
            token = urlparse.parse_qs(response)['access_token'][0]
#            print token
            return token
        except:
            print 'EXCEPTION CAUGHT!!!'
            return None
    
#    def get_url(self, path, args=None):
#        args = args or {}
#        if self._presenter._fb_access_token:
#            args['access_token'] = self._presenter._fb_access_token
#        if 'access_token' in args or 'client_secret' in args:
#            url = "https://"+self._presenter._fb_graph_url
#        else:
#            url = "http://"+self._presenter._fb_graph_url
#        return url + path + '?' + urllib.urlencode(args)
#    
#    def get(self, path, args=None):
#        return urllib2.urlopen(self.get_url(path, args=args)).read()
        
    
    def on_destroy(self, *args, **kwargs):
        print 'Destroy signal caught.'
        if self._authorized:
            print 'SUCCESS'
        else:
            print 'FAILURE'
        self.window.destroy()
        gtk.main_quit()

    def main(self):
        gobject.threads_init()
        gtk.threads_init()
        gtk.main()


if __name__ == "__main__":
#    print 'Starting app....'
    t = FBAuthWindow()
    t.main()
