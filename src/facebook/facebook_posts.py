from facebook_post import FacebookPost

class FacebookPosts:
    def __init__(self, data):
        self.posts = []
        self.previous_url = 0
        self.next_url = 0
        
        if data:
            for post in data:
                self.posts.append(FacebookPost(post))
        
        if self.posts:
            self.previous_url = self.posts[0].date_created
            self.next_url = self.posts[len(self.posts)-1].date_created
        
#        print 'PREVIOUS:', self.previous_url, 'NEXT:', self.next_url
    def to_dict(self):
        d = {}
        d['posts'] = []
        d['previous_url'] = self.previous_url
        d['next_url'] = self.next_url
        for post in self.posts:
            d['posts'].append(post.__dict__)
        return d
            
