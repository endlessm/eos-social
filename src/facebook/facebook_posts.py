from facebook_post import FacebookPost

class FacebookPosts:
    def __init__(self, data):
        self.posts = []
        self.previous_url = ''
        self.next_url = ''
        
        if data['data']:
            for post in data['data']:
                self.posts.append(FacebookPost(post))
        
        if data.has_key('paging'):
            if data['paging'].has_key('previous'):
                self.previous_url = data['paging']['previous']
            if data['paging'].has_key('next'):
                self.next_url = data['paging']['next']
            