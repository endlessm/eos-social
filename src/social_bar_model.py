import os

class SocialBarModel:
    def __init__(self):
        print 'In __init__ method.'
        self.LOCAL_FACEBOOK_FILE = os.path.expanduser('~/.fb_access_token')
        self.LOCAL_IMAGES_LOCATION = os.path.expanduser('~/.endlessm/social_bar/images/')
        
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
    
    def get_stored_picture_file_path(self):
        return self.LOCAL_IMAGES_LOCATION + 'avatar'

    def get_no_picture_file_path(self):
        return self.LOCAL_IMAGES_LOCATION + 'no_image.jpg'

