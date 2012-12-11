import gtk
import gobject
from facebook.fb_auth_view import FBAuthView
from ui import MainWindow
from ui import SimplePopUp
import webkit

#gtk.gdk.threads_init()

class SocialBarView(MainWindow):


    def __init__(self):
        super(SocialBarView, self).__init__()
        self.connect('destroy', lambda w: gtk.main_quit())

#        self._fb_auth_view = FBAuthView()
        self._presenter = None
        self._browser = webkit.WebView()

        self.btn_add = gtk.Button('FB Login')
        self.btn_add.set_size_request(64, 64)
        self.btn_add.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.btn_add.connect("button-press-event", self.__on_button_press)
        self.btn_add.show()

        self.main_container = gtk.VBox()
        self.main_container.pack_start(self.btn_add, expand=False, fill=False, padding=0)
        self.main_container.pack_start(self._browser, expand=True, fill=True, padding=0)
        self.add(self.main_container)
        self.main_container.show()
        self.show()

    def __on_button_press(self, widget, event):
#        self.show_popup_notification("test")
        print 'Button clicked, calling self._presenter.get_fb_news_feed()...'
        self._presenter.get_fb_news_feed()
        print 'DONE in click handler.'
#        self._presenter.fb_login(callback=self._presenter.get_fb_news_feed)

#    def show_fb_auth_popup(self):
#        self._fb_auth_view.open('')

    def show_popup_notification(self, notification_text):
        SimplePopUp(notification_text).show()
       
    def set_presenter(self, presenter):
        self._presenter = presenter
    
    def show_browser(self):
        self._browser.show()
    
    def load_html(self, html):
        print '='*80
        print html
        print '='*80
        result = self._browser.load_string(html, 'text/html', 'utf-8', '')
#        print 'RESULT:', result
        self.show_browser()

    def main(self):
        gobject.threads_init()
        gtk.threads_init()
        gtk.main()

