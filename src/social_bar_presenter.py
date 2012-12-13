from util.util import get_data, delete_like
from facebook.facebook import GraphAPIError, GraphAPI
from facebook.facebook_posts import FacebookPosts
from facebook.fb_auth_window import FBAuthWindow
import subprocess
from urllib2 import URLError
from Cheetah.Template import Template
import urlparse
import json
import pprint


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
        print 'In presenter.get_fb_news_feed...'
        try:
            print 'Going to FB for posts...'
            result = self._graph_api.request('/me/home')
            print 'DONE getting posts from FB, result ='#, result
        except GraphAPIError as error:
            self.oauth_exception_handler(error.result)
            return None
        except URLError as e:
            self.url_exception_handler()
            return None
        
        if result:
            print 'Converting facebook data to py objects...'
#            pprint.pprint(result)
            result = FacebookPosts(result)
#            print 'DONE converting. Result:', result
            print 'Generating html...'
            html = str(self.render_posts_to_html(result.posts))
            print 'DONE generating html.'
#            self._view.load_html(html)
            self._view.load_html(html)
            return result
        
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
                self._view.btn_add.set_label('Refresh')
            elif line.startswith('FAILURE'):
                self._view.show_popup_notification('Something went wrong when authenticating app.')

        if callback:
            callback()
    
    def post_to_fb(self, text):
#        print 'Post to Facebook.'
        try:
            self._graph_api.put_wall_post(text)
            self.get_fb_news_feed()
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
        
    def render_posts_to_html(self, posts):
        page = Template(file = 'templates/news-feed.html', searchList = [{ 'posts':posts }])
        print str(page)
        return page
    
    def navigator(self, uri):
        print 'In presenter navigator function...'
        print uri
        def register_scheme(scheme):
            for method in filter(lambda s: s.startswith('uses_'), dir(urlparse)):
                getattr(urlparse, method).append(scheme)

        register_scheme('eossocialbar')
        # parse uri
        parsed = urlparse.urlparse(uri)
        print parsed
        print 'SCHEME:', parsed.scheme
        print 'PATH  :', parsed.path
        print 'QUERY :', parsed.query
#        print 'PARAMS:', parsed.params
        parsed_query = urlparse.parse_qs(parsed.query)
        print parsed_query
        # decide which action is needed and call appropriate function
        if parsed.path == 'LIKE':
            print 'got LIKE to perform on', parsed_query['id'][0]
            result = self.post_fb_like(parsed_query['id'][0])
            print 'result:', result
            if result:
                # increase the number of likes and change to Unlike
                script = 'like_success(%s);' % json.dumps(parsed_query['id'][0])
                print 'Script tp execute:', script
                self._view._browser.execute_script(script)
        elif parsed.path == 'UNLIKE':
            print 'got UNLIKE to perform on', parsed_query['id'][0]
#            result = delete_like(self._fb_access_token, parsed_query['id'][0])
#            pprint.pprint(result)
            script = 'unlike_success(%s);' % json.dumps(parsed_query['id'][0])
            self._view._browser.execute_script(script)
        
        # execute javascript in feed web view if necessary
        return 1
        
