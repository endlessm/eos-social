from fb_auth_view import FBAuthView
from social_bar_model import SocialBarModel
from social_bar_view import SocialBarView
from util.http_request_handler import FBHTTPRequestHandler
import webbrowser
import BaseHTTPServer

class SocialBarPresenter:
    
    def __init__(self):
        self._app_id = '335071089906279'
        self._app_secret = '6fd48faa4ed1e73213a9dddb8754544a'
        self._fb_graph_url = 'graph.facebook.com'
        self._webserver_url = 'http://localhost:8080/'
        self._model = SocialBarModel()
        self._fb_access_token = self._model.get_stored_fb_access_token()
#        self.fb_auth_box = FBAuthView()
#        self._view = SocialBarView()
#        self._view.main()
#        self.fb_auth_box.open('http://google.com')
#        self.fb_auth_box.show_all()
    
#    def show_it(self):
#        self.fb_auth_box.open('http://google.com')
#        self.fb_auth_box.web_view.show()
#        self.fb_auth_box.show_all()
        
    def get_fb_news_feed(self, callback):
        token = self._model.get_stored_fb_access_token()
        if token:
            print 'Vrati niz postova'
            result = self.blah(token)
            if result:
                callback(result)
            else:
                self._view.show_popup_notification('Message text.')
        else:
            self._view.show_fb_auth_popup()
    
    def fb_login(self, callback=None):
        url = 'http://graph.facebook.com/oauth/authorize?scope=read_stream&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&client_id=335071089906279'
        print 'ORIGINAL URL:', url
        # initialize web server on port 8080
        webbrowser.open(url)
        print 'Launch localhost:8080'
        webserver = BaseHTTPServer.HTTPServer(('localhost', 8080), self.http_handler)
        
        # attach a handler for http requests
        print 'Listen for access token on 8080'
        while not self._fb_access_token:
            webserver.handle_request()
            
        # construct url for facebook login/auth
#        http://graph.facebook.com/oauth/authorize?scope=read_stream&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&client_id=335071089906279
        
        ## webbrowser for now.
#        webbrowser.open(url)
        
        # show popup with facebook login/auth page opened
#        self._view._fb_auth_view.web_view.open(url)
#        self._view._fb_auth_view.show_all()
        
#        self._view.close_fb_auth_popup()
        if callback:
            callback()
    
    def post_to_fb(self, text):
        print 'Post to Facebook.'
    
    def get_new_fb_posts(self, url):
        print 'Getting new facebook posts...'
    
    def show_fb_login(self):
        self._view.show_fb_auth_popup()
    
    def blah(self, *args):
        print '*args:', args
        return None
    
    def close_fb_auth_view(self):
        print 'Should close FB login dialogue.'
    
    def http_handler(self, *args):
        FBHTTPRequestHandler(self, *args)