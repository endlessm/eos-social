import os

class SocialBarModel:
    LOCAL_FACEBOOK_FILE = os.path.expanduser('~/.fb_access_token')
    
    def __init__(self):
        print 'In __init__ method.'
        
    def get_stored_fb_access_token(self):
        if os.path.exists(LOCAL_FACEBOOK_FILE):
            return open(LOCAL_FACEBOOK_FILE).read()
        else:
            return None
    
    def save_fb_access_token(self, token):
        if token:
            try:
                open(LOCAL_FACEBOOK_FILE,'w').write(token)
                return True
            except:
                return False
        else:
            return False
    
    