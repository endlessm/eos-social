import gtk
import gobject
from facebook.fb_auth_view import FBAuthView
from ui import MainWindow
from ui import SimplePopUp
import webkit
from ui import PostMessage
from ui import PostMessageSendArea
from ui import UserAvatar

#gtk.gdk.threads_init()

class SocialBarView(MainWindow):


    def __init__(self):
        super(SocialBarView, self).__init__()
        self.connect('destroy', lambda w: gtk.main_quit())

#        self._fb_auth_view = FBAuthView()
        self._presenter = None
        self._browser = webkit.WebView()
#        self._browser.set_size_request(-1, 600)
        self._browser.connect("navigation-requested", self._navigation_handler)

        self.btn_add = gtk.Button('Login')
        self.btn_add.set_size_request(64, 64)
        self.btn_add.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.btn_add.connect("button-press-event", self.__on_button_press)
        self.btn_add.show()

        self.post_message_area = PostMessageSendArea()
        self.user_avatar = UserAvatar()
        #self.user_avatar.set_avatar('avatar.png')
        self.post_message_area.connect('post-panel-action', self._on_action)
        self.post_message = PostMessage(self.post_message_area, self.user_avatar)
        self.post_message.connect('post-panel-action', self._on_action)

        # pack web container
        self.web_container = gtk.VBox()
        self.web_container.pack_start(self.btn_add, expand=False, fill=False, padding=0)
        self.web_container.pack_start(self._browser, expand=True, fill=True, padding=0)

        # pack main container
        self.main_container = gtk.VBox()
        self.main_container.pack_start(self.post_message, expand=False, fill=False, padding=0)
        self.main_container.pack_start(self.web_container, expand=True, fill=True, padding=0)
        self.add(self.main_container)
        self.main_container.show()
        self.show_all()

    def _on_action(self, widget, action):
        if action == 'post':
            self.post_message.toggle_text_field()
            self.post_message_area.set_default_text()
        elif action == 'cancel':
            self.post_message.collapse_text_field()
            self.post_message_area.set_default_text()
        elif action == 'close':
            gtk.main_quit()
        elif action == 'send':
            text = self.post_message_area.get_post_message()
            self.post_message_area.set_default_text()
            if text is not None:
                self._presenter.post_to_fb(text)
        elif action == 'avatar':
            self._presenter.show_profil_page()
        else:
            pass

    #def _print(self):
    #    print '!'
    #    return True

    #def _animate(self):
    #    self._h += 5
    #    self.post_message.set_size_request(-1, self._h)
    #    if self._h < 200:
    #        return True
    #    self.post_message.show_text_field()
    #    return False

    def __on_button_press(self, widget, event):

#        self.show_popup_notification("test")
        if self.btn_add.get_label() == 'Login':
#            print 'Button clicked, calling self._presenter.get_fb_news_feed()...'
            self._presenter.fb_login(callback=self._presenter.get_fb_news_feed)
#            print 'DONE in click handler.'
        else:
            self._presenter.get_fb_news_feed()

#    def show_fb_auth_popup(self):
#        self._fb_auth_view.open('')

    def show_popup_notification(self, notification_text):
        SimplePopUp(notification_text).show()
       
    def set_presenter(self, presenter):
        self._presenter = presenter
        def _update_image():
            print 'update image'
            self.user_avatar.set_avatar(self._presenter.get_stored_picture_file_path())
        user_image = self._presenter.get_profil_picture(callback=_update_image)
        self.user_avatar.set_avatar(self._presenter.get_stored_picture_file_path())
    
    def show_browser(self):
        self._browser.show()
    
    def load_html(self, html):
#        print '='*80
#        print html
#        print '='*80
        result = self._browser.load_string(html, 'text/html', 'utf-8', '')
#        print 'RESULT:', result
        self.show_browser()
    
    def _navigation_handler(self, view, frame, request, data=None):
        print 'In navigation handler view function...'
        return self._presenter.navigator(request.get_uri())

    def main(self):
        gobject.threads_init()
        gtk.threads_init()
        gtk.main()

