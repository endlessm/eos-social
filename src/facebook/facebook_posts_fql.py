from facebook_post_fql import FacebookPostFql

class FacebookPostsFql:
    def __init__(self, data):
        self.posts = []
        self.previous_url = 0
        self.next_url = 0
        
        if data:
            for post in data:
                self.posts.append(FacebookPostFql(post))
        
        if self.posts:
            self.previous_url = self.posts[0].date_created
            self.next_url = self.posts[len(self.posts)-1].date_created
        
        print 'PREVIOUS:', self.previous_url, 'NEXT:', self.next_url
        
#        if data.has_key('paging'):
#            if data['paging'].has_key('previous'):
#                self.previous_url = data['paging']['previous']
#            if data['paging'].has_key('next'):
#                self.next_url = data['paging']['next']
            