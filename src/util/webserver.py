from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from facebook.facebook import GraphAPIError, GraphAPI
from util import posts_query, users_query, older_posts_query, newer_posts_query
from facebook.facebook_posts import FacebookPosts
from social_bar_model import SocialBarModel
import json
import simplejson
import urlparse
import gettext
import pprint
from Cheetah.Template import Template

gettext.install('eos-social', '/usr/share/locale', unicode=True, names=['ngettext'])

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)

        parsed_qry = urlparse.parse_qs(parsed_path.query)
        jsonp_string = parsed_qry['onJSONPLoad'][0]
        timestamp = parsed_qry['timestamp'][0]
        
        if 'newer' in parsed_path.path.lower():
            fb_response = self.get_new_fb_posts(timestamp, False)
        elif 'older' in parsed_path.path.lower():
            fb_response = self.get_new_fb_posts(timestamp, True)
        else:
            fb_response = None
        
        if not fb_response:
            posts = {}
        else:
            posts = self.parse_posts(fb_response)
        
        html = self.generate_posts_elements(posts.posts)
        data = {}
        data['html'] = str(html)
        if 'older' in parsed_path.path.lower():
            data['next_url'] = posts.next_url
        else:
            data['previous_url'] = posts.previous_url
            
        to_write = jsonp_string + '(' + simplejson.dumps(data) + ')'
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(to_write)
        
        return 

    def do_POST(self):
        return
    
    def get_new_fb_posts(self, stamp, older=True):
        if older:
            query = {'posts':older_posts_query % str(stamp),'users':users_query}
        else:
            query = {'posts':newer_posts_query % str(stamp),'users':users_query}
        try:
            _model = SocialBarModel()
            _token = _model.get_stored_fb_access_token()
            _graph_api = GraphAPI(access_token=_token)
            result = _graph_api.fql(query)
            return result
        except:
            #print 'exception caught'
            return None
    
    def parse_posts(self, result):
        posts = []
        users = []
        for res_set in result:
            if res_set['name'] == 'posts':
                posts = res_set['fql_result_set']
            else:
                users = res_set['fql_result_set']
        
        for post in posts:
            for user in users:
                if post['actor_id'] == user['id']:
                    post['who'] = user
                    break
        
        return FacebookPosts(posts)
    
    def generate_posts_elements(self, posts):
        params = [{'posts':posts},
                  {'like_string':_('like')},
                  {'comment_string':_('comment')}]
        page = Template(file = '/usr/share/eos-social/templates/posts-array.html', searchList = params)
        return page
        
def main():
    try:
        server = HTTPServer(('', 8088), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

