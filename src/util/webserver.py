from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from facebook.facebook import GraphAPIError, GraphAPI
from util import posts_query, users_query, older_posts_query, newer_posts_query, comments_query, comments_users_query
from facebook.facebook_posts import FacebookPosts
from social_bar_model import SocialBarModel
import json
import simplejson
import urlparse
import gettext
import pprint
from Cheetah.Template import Template
from settings import Settings

gettext.install('eos-social', '/usr/share/locale', unicode=True, names=['ngettext'])

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        parsed_qry = urlparse.parse_qs(parsed_path.query)
        jsonp_string = parsed_qry['onJSONPLoad'][0]
        
        print '-'*80
        print 'PARSED PATH :', parsed_path
        print 'PARSED QUERY:', parsed_qry
        print 'JSONP STRING:', jsonp_string
        print '-'*80
        if 'newer' in parsed_path.path.lower():
            timestamp = parsed_qry['timestamp'][0]
            fb_response = self.get_new_fb_posts(timestamp, False)
        elif 'older' in parsed_path.path.lower():
            timestamp = parsed_qry['timestamp'][0]
            fb_response = self.get_new_fb_posts(timestamp, True)
        elif 'comment' in parsed_path.path.lower():
            postid = parsed_qry['id'][0]
            fb_response = self.get_comments(postid, int(parsed_qry['time'][0]))
        else:
            fb_response = None
        
        if not fb_response:
            posts = {}
        else:
            if 'comment' not in parsed_path.path.lower():
                posts = self.parse_posts(fb_response)
        
        data = {}
        
        if 'older' in parsed_path.path.lower():
            html = self.generate_posts_elements(posts.posts)
            data['html'] = str(html)
            data['next_url'] = posts.next_url
        elif 'newer' in parsed_path.path.lower():
            html = self.generate_posts_elements(posts.posts)
            data['html'] = str(html)
            data['previous_url'] = posts.previous_url
        elif 'comment' in parsed_path.path.lower():
#            data = fb_response
            data['html'] = str(self.generate_comments(fb_response, parsed_qry['id'][0], int(parsed_qry['time'][0])))
            data['html'] = data['html'].replace('\n','')
            print '+'*80
            print data['html']
            print '+'*80
            print '+'*80
            print simplejson.dumps(data['html'])
            print '+'*80
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
                  {'comment_string':_('comment')},
                  {'auto_refresh_interval':Settings.FB_AUTO_REFRESH_INTERVAL}]
        page = Template(file = '/usr/share/eos-social/templates/posts-array.html', searchList = params)
        return page
    
    def get_comments(self, post_id, until=0):
        if until:
            cqry = comments_query % ('483083671730084 AND time < ' + str(until), '10')
        else:
            cqry = comments_query % ('483083671730084', '10')
        
        query = {'comments':cqry,'users':comments_users_query}
        try:
            _model = SocialBarModel()
            _token = _model.get_stored_fb_access_token()
            _graph_api = GraphAPI(access_token=_token)
            result = _graph_api.fql(query)
#            print 'In get_comments...'
#            print '-'*80
#            pprint.pprint(result)
#            print '-'*80
            comments = self.parse_comments(result)
            print 'In get_comments...'
            print cqry
            print '-'*80
            pprint.pprint(comments)
            print '-'*80
        except GraphAPIError as error:
            print 'GRAPH API ERROR CAUGHT!'
            print '-'*80
            pprint.pprint(error)
            print '-'*80
            self.oauth_exception_handler(error.result)
            return None
        except URLError as e:
            self.url_exception_handler()
            return None
        except:
            return None
            
        return comments
    
    def parse_comments(self, data):
        comments = []
        users = []
        
        for _set in data:
            if _set['name'] == 'comments':
                comments = _set['fql_result_set']
            else:
                users = _set['fql_result_set']
        
        for comment in comments:
            for user in users:
                if comment['fromid'] == user['uid']:
                    comment['from'] = user
                    break
#        print 'In parse_comments...'
#        print '-'*80
#        pprint.pprint(comments)
#        print '-'*80
        comments.reverse()
        return comments
    
    def generate_comments(self, comments, post_id, time):
        pprint.pprint(comments)
        print '*'*80
        print post_id
        print '*'*80
        print time
        print '*'*80
        params = [{"comments":comments},
                  {"post_id":post_id},
                  {"comments_page_size":10},
                  {"initial_comments_number":4}]
        if time == 0:
            params.append({'first_batch':True})
        else:
            params.append({'first_batch':False})\
        
        if len(comments) < 10:
            params.append({'has_more_comments':False})
            params.append({'last_comment_time':0})
        else:
            params.append({'has_more_comments':True})
            params.append({'last_comment_time':comments[0]['time']})
        pprint.pprint(params)
        print '*'*80
        page = Template(file = '/usr/share/eos-social/templates/comments-blank.html', searchList = params)
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

