from gi.repository import Gtk
from gi.repository import GObject
from ui.main_window import MainWindow
from gi.repository import WebKit
import gettext


gettext.install('eos-social', '/usr/share/locale', unicode=True, names=['ngettext'])

ALT = '<Alt>'

class SocialBarView(MainWindow):
    

    def __init__(self):
        super(SocialBarView, self).__init__()
        self.connect('destroy', self._destroy)
        self.set_title('Endless Social Bar')
        self._create()

    def create_shortcuts(self, accelgroup=Gtk.AccelGroup()):
        for hotkey, modifier, callback in self._shortcuts:
            key, modifier = Gtk.accelerator_parse(modifier + hotkey)
            accelgroup.connect(key, modifier, Gtk.AccelFlags.VISIBLE, callback)
        self.add_accel_group(accelgroup)

    def _create(self):
        self._browser = WebKit.WebView()
        self._browser.connect("navigation-requested", self._navigation_handler)
        self._shortcuts = [('Left', ALT, lambda a, widget, c, m: self._browser.go_back()),
                           ('Right', ALT, lambda a, widget, c, m: self._browser.go_forward())]
        self.create_shortcuts()

        self.main_container = Gtk.ScrolledWindow()
        self.main_container.add(self._browser)

        self.add(self.main_container)
        self.show_all()
        self.hide()

        self._browser.load_uri('http://m.facebook.com')

    def _navigation_handler(self, view, frame, request, data=None):
        return False
    
    def _destroy(self, *args):
        Gtk.main_quit()

    def main(self):
        GObject.threads_init()
        Gtk.main()
