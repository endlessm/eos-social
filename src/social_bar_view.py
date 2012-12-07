import gtk
import gobject
from facebook.fb_auth_view import FBAuthView
from ui import MainWindow
from ui import SimplePopUp

#gtk.gdk.threads_init()

class SocialBarView(MainWindow):


    def __init__(self):
        super(SocialBarView, self).__init__()
        self.connect('destroy', lambda w: gtk.main_quit())

        self._fb_auth_view = FBAuthView()

        btn_add = gtk.Button()
        btn_add.set_size_request(64, 64)
        btn_add.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        btn_add.connect("button-press-event", self.__on_button_press)

        main_container = gtk.VBox()
        main_container.pack_start(btn_add, expand=False, fill=False, padding=0)
        self.add(main_container)
        self.show_all()

    def __on_button_press(self, widget, event):
        self.show_popup_notification("test")

    def show_fb_auth_popup(self):
        self._fb_auth_view.open('')

    def show_popup_notification(self, notification_text):
        SimplePopUp(notification_text).show()

    def main(self):
        gobject.threads_init()
        gtk.threads_init()
        gtk.main()

