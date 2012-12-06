from social_bar_model import SocialBarModel
from util.http_request_handler import FBHTTPRequestHandler
from util.social_bar_http_server import SocialBarHttpServer
from util.util import get_data, fb_auth_url
from facebook.facebook import GraphAPIError, GraphAPI
import webbrowser
import pprint
from facebook.facebook_posts import FacebookPosts


class SocialBarPresenter:
    
    def __init__(self, view=None, model=None):
        # -- DEV --
        self._app_id = '393860344022808'
        self._app_secret = 'eb0dcb05f7512be39f7a3826ce99dfcd'
        # -- PRODUCTION --
#        self._app_id = ''
#        self._app_secret = ''
        self._fb_graph_url = 'graph.facebook.com'
        self._webserver_url = 'http://localhost:8080/'
        self._model = SocialBarModel()
        self._fb_access_token = self._model.get_stored_fb_access_token()
        if self._fb_access_token:
            self._graph_api = GraphAPI(access_token=self._fb_access_token)
        else:
            self._graph_api = None
        
    def get_fb_news_feed(self, callback):
        if self._fb_access_token:
            if not self._graph_api:
                self._graph_api = GraphAPI(access_token=self._fb_access_token)
            
            try:
                result = self._graph_api.request('/me/home')
            except GraphAPIError as error:
                print error.result
                # Do I need to show login/auth automatically or just to inform a user?
                # This decision obviously depends on error received!
                return None
            
            if result:
#                pprint.pprint(result)
                result = FacebookPosts(result)
            
            if callback:
                callback(result)
            else:
                return result
#            else:
#                self._view.show_popup_notification('Message text.')
#        else:
#            self._view.show_fb_auth_popup()
    
            
                
    
    def fb_login(self, callback=None):
        url = fb_auth_url(self._app_id, self._webserver_url, ['read_stream','publish_stream'])
        # self._view.show_fb_auth_popup(url)
        webbrowser.open(url)
        webserver = SocialBarHttpServer(('localhost', 8080), self.http_handler)
        webserver.serve_forever()

        if callback:
            callback()
    
    def post_to_fb(self, text):
        print 'Post to Facebook.'
        self._graph_api = GraphAPI(access_token=self._fb_access_token)
        
        try:
            self._graph_api.put_wall_post(text)
            return True
        except GraphAPIError as error:
            print error.result
            return False
    
    def post_fb_like(self, id):
        print 'Posting like to post with id', id
        self._graph_api = GraphAPI(access_token=self._fb_access_token)
        
        try:
            self._graph_api.put_like(id)
            return True
        except GraphAPIError as error:
            print error.result
            return False
    
    def post_fb_comment(self, id, comment):
        print 'Posting comment (',comment,') to post with id', id
        self._graph_api = GraphAPI(access_token=self._fb_access_token)
        
        try:
            self._graph_api.put_comment(id, comment)
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
            else:
                return result
    
    def show_fb_login(self):
        self._view.show_fb_auth_popup()
    
    def blah(self, *args):
        print '*args:', args
        return None
    
    def close_fb_auth_view(self):
        print 'Should close FB login dialogue.'
#        self._view.close_fb_auth_popup()
    
    def http_handler(self, *args):
        FBHTTPRequestHandler(self, *args)
    
    def set_fb_access_token(self, token):
        self._fb_access_token = token
        self._model.save_fb_access_token(token)
    
    def print_posts(self, result):
        print 'FOUND', str(len(result.posts)), 'POSTS...'
        print '='*80
        for post in result.posts:
            print unicode(post)
        print 'next_url     :', result.next_url
        print '='*80
        print 'previous_url :', result.previous_url
        print '='*80