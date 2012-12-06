import os

class SocialBarModel:
    def __init__(self):
        print 'In __init__ method.'
        self.LOCAL_FACEBOOK_FILE = os.path.expanduser('~/.fb_access_token')
        
    def get_stored_fb_access_token(self):
        if os.path.exists(self.LOCAL_FACEBOOK_FILE):
            return open(self.LOCAL_FACEBOOK_FILE).read()
        else:
            return None
    
    def save_fb_access_token(self, token):
        if token:
            try:
                open(self.LOCAL_FACEBOOK_FILE,'w').write(token)
                return True
            except:
                return False
        else:
            return False
    
    