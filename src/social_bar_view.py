import gtk
import gobject
import signal
import time
import Queue
import thread
import webkit

from facebook.fb_auth_view import FBAuthView
from ui import MainWindow
from ui import SimplePopUp
import webkit
from ui import PostMessage
from ui import PostMessageSendArea
import os
from ui import UserAvatar


class SocialBarView(MainWindow):

    @classmethod
    def main_wraper(cls, fun, quit_obj=None):
        signal.signal(signal.SIGINT, quit_obj.set_quit)
        def fun2(*args, **kwargs):
            try:
                x = fun(*args, **kwargs) # equivalent to "apply"
            finally:
                cls.kill_gtk_thread()
                quit_obj.set_quit()
            return x
        return fun2

<<<<<<< HEAD
    def __init__(self):
        super(SocialBarView, self).__init__()
        self.connect('destroy', self._destroy)

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
=======
    @classmethod
    def start_gtk_thread(cls):
        # Start GTK in its own thread:
        gtk.gdk.threads_init()
        thread.start_new_thread(gtk.main, ())

    @classmethod
    def kill_gtk_thread(cls):
        cls.asynchronous_gtk_message(gtk.main_quit)()

    @classmethod
    def asynchronous_gtk_message(cls, fun):
        def worker((function, args, kwargs)):
            apply(function, args, kwargs)
        def fun2(*args, **kwargs):
            gobject.idle_add(worker, (fun, args, kwargs))
        return fun2

    @classmethod
    def synchronous_gtk_message(cls, fun):
        class NoResult: pass
        def worker((R, function, args, kwargs)):
            R.result = apply(function, args, kwargs)
        def fun2(*args, **kwargs):
            class R: result = NoResult
            gobject.idle_add(worker, (R, fun, args, kwargs))
            while R.result is NoResult: time.sleep(0.01)
            return R.result
        return fun2

    def __init__(self, uri, quit_function):
        super(SocialBarView, self).__init__()
        self._browser = webkit.WebView()
        self._uri = uri
        self._quit_function = quit_function
        #
        self._presenter = None
        #
        self.message_queue = Queue.Queue()
        if self._quit_function is not None:
            self.connect('destroy', self._quit_function)

        def title_changed(title):
            if title != 'null': self.message_queue.put(title)

        # create window layout
        btn_add = gtk.Button()
        btn_add.set_size_request(64, 64)
        btn_add.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        btn_add.connect("button-press-event", self.__on_button_press)

        main_container = gtk.VBox(homogeneous=False, spacing=0)
        main_container.pack_start(btn_add, expand=False, fill=False, padding=0)
        main_container.pack_start(self._browser, expand=True, fill=True, padding=0)
        self.add(main_container)
        self.show_all()

        self.connect_title_changed(title_changed)
        self.open_uri(self._uri)
>>>>>>> github/dev

    def __on_button_press(self, widget, event):

<<<<<<< HEAD
#        self.show_popup_notification("test")
        if self.btn_add.get_label() == 'Login':
#            print 'Button clicked, calling self._presenter.get_fb_news_feed()...'
            self._presenter.fb_login(callback=self._presenter.get_fb_news_feed)
#            print 'DONE in click handler.'
        else:
            self._presenter.get_fb_news_feed()

#    def show_fb_auth_popup(self):
#        self._fb_auth_view.open('')
=======
    def show_fb_auth_popup(self):
        FBAuthView().open('')
>>>>>>> github/dev

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
    
    def _destroy(self, *args):
        os.remove(os.path.expanduser('~/.fb_access_token'))
        gtk.main_quit()

    def connect_title_changed(self, callback):
        self._browser.connect(
            'title-changed', 
            lambda widget, frame, title: callback(title)
            )

    def open_uri(self, uri):
        self._browser.open(uri)
    
    def web_recv(self):
        if self.message_queue.empty():
            return None
        msg = self.message_queue.get()
        print '>>>', msg
        return msg

    def web_send(self, msg):
        print '<<<', msg
        self.asynchronous_gtk_message(self._browser.execute_script)(msg)
