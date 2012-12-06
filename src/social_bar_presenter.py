#from facebook.fb_auth_view import FBAuthView
from social_bar_model import SocialBarModel
#from social_bar_view import SocialBarView
from util.http_request_handler import FBHTTPRequestHandler
from util.util import get_data
from facebook.facebook import GraphAPIError, GraphAPI, auth_url
import webbrowser
import BaseHTTPServer
#import pprint
#from facebook.facebook_post import FacebookPost
from facebook.facebook_posts import FacebookPosts


class SocialBarPresenter:
    
    def __init__(self, view=None, model=None):
        self._view = view
        self._model = model
        # -- DEV --
        self._app_id = '393860344022808'
        self._app_secret = 'eb0dcb05f7512be39f7a3826ce99dfcd'
        # -- PRODUCTION --
#        self._app_id = ''
#        self._app_secret = ''
        self._fb_graph_url = 'graph.facebook.com'
        self._webserver_url = 'http://localhost:8080/'
        self._fb_access_token = self._model.get_stored_fb_access_token()
        if self._fb_access_token:
            self._graph_api = GraphAPI(access_token=self._fb_access_token)
        else:
            self._graph_api = None
#        self.fb_auth_box = FBAuthView()
#        self._view = SocialBarView()
#        self._view.main()
#        self.fb_auth_box.open('http://google.com')
#        self.fb_auth_box.show_all()
    
#    def show_it(self):
#        self.fb_auth_box.open('http://google.com')
#        self.fb_auth_box.web_view.show()
#        self.fb_auth_box.show_all()

    def get_view(self):
        return self._view

    def get_model(self):
        return self._model
        
    def get_fb_news_feed(self, callback):
        if self._fb_access_token:
            if not self._graph_api:
                self._graph_api = GraphAPI(access_token=self._fb_access_token)
            
            try:
                result = self._graph_api.request('/me/home')
            except GraphAPIError as error:
                print error.result
#                self._view.show_popup_notification('Message text.')
                return None
            
            if result:
                result = FacebookPosts(result)
            
            if callback:
                callback(result)
            else:
                return result
#            else:
#                self._view.show_popup_notification('Message text.')
#        else:
#            self._view.show_fb_auth_popup()
    
#    def get_new_fb_posts(self, callback, url):
#        if self._fb_access_token:
#            if not self._graph_api:
#                self._graph_api = GraphAPI(access_token=self._fb_access_token)
#
#            result = get_data(url)
#            print result
#            # @TODO: check for error
#            if callback:
#                callback(result)
            
                
    
    def fb_login(self, callback=None):
        url = auth_url(self._app_id, self._webserver_url, ['read_steam','publish_stream'])
        print 'OAuth URL:', url
        url = 'http://graph.facebook.com/oauth/authorize?scope=publish_actions,read_stream&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&client_id=393860344022808'
        #print 'ORIGINAL URL:', url
        # initialize web server on port 8080
        webbrowser.open(url)
        #print 'Launch localhost:8080'
        webserver = BaseHTTPServer.HTTPServer(('localhost', 8080), self.http_handler)
        
        # attach a handler for http requests
        # print 'Listen for access token on 8080'
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
        
        return
    
    def post_to_fb(self, text):
        print 'Post to Facebook.'
        if self._fb_access_token:
            if not self._graph_api:
                self._graph_api = GraphAPI(access_token=self._fb_access_token)
        
        try:
            self._graph_api.put_wall_post(text)
            return True
        except GraphAPIError as error:
            print error.result
            return False
    
    def post_fb_like(self, id):
        print 'Posting like to post with id', id
        if self._fb_access_token:
            if not self._graph_api:
                self._graph_api = GraphAPI(access_token=self._fb_access_token)
        
        try:
            self._graph_api.put_like(id)
            return True
        except GraphAPIError as error:
            print error.result
            return False
    
    def get_new_fb_posts(self, callback, url):
        print 'Getting new facebook posts...'
        if self._fb_access_token:
            if not self._graph_api:
                self._graph_api = GraphAPI(access_token=self._fb_access_token)

            result = get_data(url)
            if result:
                result = FacebookPosts(result)
            # @TODO: check for error
            if callback:
                callback(result)
    
    def show_fb_login(self):
        self._view.show_fb_auth_popup()
    
    def blah(self, *args):
        print '*args:', args
        return None
    
    def close_fb_auth_view(self):
        print 'Should close FB login dialogue.'
    
    def http_handler(self, *args):
        FBHTTPRequestHandler(self, *args)
    
    def print_posts(self, result):
        print 'FOUND', str(len(result.posts)), 'POSTS...'
        print '='*80
        for post in result.posts:
            print unicode(post)
        print 'next_url     :', result.next_url
        print '='*80
        print 'previous_url :', result.previous_url
        print '='*80