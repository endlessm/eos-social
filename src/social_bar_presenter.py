import time
import json

from social_bar_model import SocialBarModel
from util.http_request_handler import FBHTTPRequestHandler
from util.social_bar_http_server import SocialBarHttpServer
from util.util import get_data, fb_auth_url
from facebook.facebook import GraphAPIError, GraphAPI
from facebook.facebook_posts import FacebookPosts
from facebook.fb_auth_window import FBAuthWindow
import subprocess
from urllib2 import URLError


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

    def get_view(self):
        return self._view

    def get_model(self):
        return self._model

    def get_fb_news_feed(self, callback=None):
        try:
            result = self._graph_api.request('/me/home')
        except GraphAPIError as error:
            self.oauth_exception_handler(error.result)
            return None
        except URLError as e:
            self.url_exception_handler()
            return None
        
        if result:
            result = FacebookPosts(result)
        
        if callback:
            callback(result)
        else:
            return result
    
    def fb_login(self, callback=None):
#        url = fb_auth_url(self._app_id, self._webserver_url, ['read_stream','publish_stream'])
        proc = subprocess.Popen(['python', 'facebook/fb_auth_window.py'], stdout=subprocess.PIPE)
        for line in proc.stdout:
            print line
            if line.startswith('ACCESS_TOKEN:'):
                token = line.split(':')[1]
                self.set_fb_access_token(token)
                self._graph_api = GraphAPI(access_token=self._fb_access_token)
            elif line.startswith('FAILURE'):
                self._view.show_popup_notification('Something went wrong when authenticating app.')

        if callback:
            callback()

    def post_to_fb(self, text):
#        print 'Post to Facebook.'
        try:
            self._graph_api.put_wall_post(text)
            return True
        except GraphAPIError as error:
            self.oauth_exception_handler(error.result)
            return False
        except URLError as e:
            self.url_exception_handler()
            return False
        except:
            return False
    
    def post_fb_like(self, id):
#        print 'Posting like to post with id', id        
        try:
            self._graph_api.put_like(id)
            return True
        except GraphAPIError as error:
            self.oauth_exception_handler(error.result)
            return False
        except URLError as e:
            self.url_exception_handler()
            return False
        except:
            return False
    
    def post_fb_comment(self, id, comment):
#        print 'Posting comment (',comment,') to post with id', id        
        try:
            self._graph_api.put_comment(id, comment)
            return True
        except GraphAPIError as error:
#            print error.result
            self.oauth_exception_handler(error.result)
            return False
        except URLError as e:
            self.url_exception_handler()
            return False
        except:
            return False
        
    def get_new_fb_posts(self, callback, url):
#        print 'Getting new facebook posts...'
            result = get_data(url)
            if result:
                result = FacebookPosts(result)
            else:
                self.url_exception_handler()
            if callback:
                callback(result)
            else:
                return result

    def show_fb_login(self):
        self._view.show_fb_auth_popup()

    def set_fb_access_token(self, token):
        self._fb_access_token = token
        self._model.save_fb_access_token(token)

    def oauth_exception_handler(self, result):
        server_error_codes = [1,2,4,17]
        oauth_error_codes = [102, 190]
        permissions_error_codes = range(200, 300)
        
        code = result['code']
        if code in server_error_codes:
            #@TODO: Internationalization!
            message = 'Requested action is not possible at the moment. Please try again later.'
            self._view.show_popup_notification(message)
        if code in oauth_error_codes or code in permissions_error_codes:
            self.fb_login()
    
    def url_exception_handler(self):
        #@TODO: Internationalization!
        message = 'Network problem detected. Please check your internet connection and try again.'
        self._view.show_popup_notification(message)
    
    def print_posts(self, result):
        #@TODO: needed for development, remove from final version
        if not result:
            print 'NO RESULT TO PRINT.'
            return
        print 'FOUND', str(len(result.posts)), 'POSTS...'
        print '='*80
        for post in result.posts:
            print unicode(post)
        print 'next_url     :', result.next_url
        print '='*80
        print 'previous_url :', result.previous_url
        print '='*80

    def main(self, quit_obj=None):
        self._quit_obj = quit_obj
        last_second = time.time()
        uptime_seconds = 1
        clicks = 0

        while not self._quit_obj.quit:
            current_time = time.time()
            again = False
            msg = self._view.web_recv()
            if msg:
                msg = json.loads(msg)
                again = True

            if msg == "got-a-click":
                self._view.show_popup_notification("Simple PopUp")

            if current_time - last_second >= 1.0:
                self._view.web_send(
                    'document.getElementById("uptime-value").innerHTML = %s' % 
                    json.dumps('%d' % current_time)
                    )
                last_second += 1.0

            if not again:
                time.sleep(0.1)
