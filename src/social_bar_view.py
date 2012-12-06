import gtk
import gobject
from facebook.fb_auth_view import FBAuthView

#gtk.gdk.threads_init()

class SocialBarView(gtk.Window):
    
    def __init__(self):
        print 'Social Bar Construtor...'
        self._fb_auth_view = FBAuthView()
        
    def show_fb_auth_popup(self):
        self._fb_auth_view.open('')
        
    
    def show_popup_notification(self, notification_text):
        print 'User notification should be displayed.'
    
    def main(self):
        gobject.threads_init()
        gtk.threads_init()
        gtk.main()