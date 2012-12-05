import gtk
from fb_auth_view import FBAuthView

class SocialBarView(gtk.Window):
    
    def __init__(self):
        print 'Social Bar Construtor...'
        
    def show_fb_auth_popup(self):
        print 'Should show FB login/auth dialogue.'
    
    def show_popup_notification(self, notification_text):
        print 'User notification should be displayed.'
    