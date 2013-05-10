import gtk
import gobject
import os
from wm_inspect import WM_Inspect_MixIn


class MainWindow(gtk.Window, WM_Inspect_MixIn):

    WIDTH = 400
    #FIXME: we should use the primary monitor workarea
    BOTTOM_OFFSET = 38

    def __init__(self):
        gtk.Window.__init__(self, 
                            type=Gtk.WindowType.TOPLEVEL,
                            decorated=False,
                            modal=True,
                            resizable=False,
                            skip_pager_hint=True,
                            skip_taskbar_hint=True)
        WM_Inspect_MixIn.__init__(self)

        # stick on all desktops
        self.stick()
        # do not destroy on delete event
        self.connect('delete-event', lambda w, e: self.hide_on_delete())

    #FIXME: this is still pretty awful
    def _active_win_callback(self, active_name):
        if active_name != self.get_title():
            self.hide()

    def _ensure_position(self):
        width = MainWindow.WIDTH
        height = gtk.gdk.screen_height() - MainWindow.BOTTOM_OFFSET
        x = gtk.gdk.screen_width() - width
        y = 0

        self.move(x, y)
        self.set_size_request(width, height)

    def show(self):
        self._ensure_position()
        self.present()

    def hide(self):
        self.iconify()
