from fb_auth_view import FBAuthView
from social_bar_model import SocialBarModel
from social_bar_view import SocialBarView

class SocialBarPresenter:
    
    def __init__(self):
        self._model = SocialBarModel()
        self.fb_auth_box = FBAuthView()
        self._view = SocialBarView()
#        self.fb_auth_box.open('http://google.com')
#        self.fb_auth_box.show_all()
    
    def show_it(self):
        self.fb_auth_box.open('http://google.com')
        self.fb_auth_box.web_view.show()
        self.fb_auth_box.show_all()
        
    def get_fb_news_feed(self, callback):
        token = self._model.get_stored_fb_access_token()
        if token:
            print 'Vrati niz postova'
            result = blah(token)
            if result:
                callback(result)
            else:
                self._view.show_popup_notification('Message text.')
        else:
            self._view.show_fb_auth_popup()
    
    def fb_login(self, callback=None):
        self._view.show_fb_auth_popup()
        print 'Launch localhost:8080'
        print 'Listen for access token on 8080'
        self._view.close_fb_auth_popup()
        if callback:
            callback()
    
    def post_to_fb(self, text):
        print 'Post to Facebook.'
    
    def get_new_fb_posts(self, url):
        p