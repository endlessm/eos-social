import gtk
import gobject
from ui.main_window import MainWindow
import webkit
from ui import MultiPanel
import gettext
import time
from settings import Settings
import os
import json

gettext.install('eos-social', '/usr/share/locale', unicode=True, names=['ngettext'])

ALT = '<Alt>'

class SocialBarView(MainWindow):
    

    def __init__(self):
        super(SocialBarView, self).__init__()
        self.connect('destroy', self._destroy)
        self.set_title(Settings.MAIN_WINDOW_TITLE)
        super(SocialBarView, self).set_ignore_win_names(Settings.IGNORE_WIN_NAMES)

        self._create()

    def create_shortcuts(self, accelgroup=gtk.AccelGroup()):
        for hotkey, modifier, callback in self._shortcuts:
            key, modifier = gtk.accelerator_parse(modifier + hotkey)
            accelgroup.connect_group(key, modifier, gtk.ACCEL_VISIBLE, callback)
        self.add_accel_group(accelgroup)

    def _create(self):
        self._browser = webkit.WebView()
        self._browser.connect("navigation-requested", self._navigation_handler)
        self._shortcuts = [('Left', ALT, lambda a, widget, c, m: self._browser.go_back()),
                           ('Right', ALT, lambda a, widget, c, m: self._browser.go_forward())]
        self.create_shortcuts()

        self.main_container = gtk.ScrolledWindow()
        self.main_container.add(self._browser)

        self.wraper_main = MultiPanel()
        self.wraper_main.add_panel(self.main_container, 'main_container')
        self.add(self.wraper_main)
        self.show_all()
        self.hide()

        self._browser.load_uri('http://m.facebook.com')

    def _navigation_handler(self, view, frame, request, data=None):
        return False
    
    def _destroy(self, *args):
        gtk.main_quit()

    def main(self):
        gobject.threads_init()
        gtk.threads_init()
        gtk.main()

