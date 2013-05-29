
from gi.repository import Gdk
from gi.repository import GdkX11
from gi.repository import Gtk
from wm_inspect import WM_Inspect_MixIn

class MainWindow(Gtk.Window, WM_Inspect_MixIn):

    def __init__(self):
        Gtk.Window.__init__(self, 
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

        # update position when workarea changes
        screen = Gdk.Screen.get_default()
        screen.connect('monitors-changed', self._on_monitors_changed)

    def _active_win_callback(self, active_xid):
        xid = GdkX11.X11Window.get_xid(self.get_window())
        if xid != active_xid:
            self.hide()

    def _on_monitors_changed(self, screen, data):
        self._ensure_position()

    def _ensure_position(self):
        screen = Gdk.Screen.get_default()
        monitor = screen.get_primary_monitor()
        workarea = screen.get_monitor_workarea(monitor)

        width = workarea.width / 3

        geometry = Gdk.Rectangle()
        geometry.x = workarea.x + workarea.width - width
        geometry.y = workarea.y
        geometry.width = width
        geometry.height = workarea.height

        self.move(geometry.x, geometry.y)
        self.set_size_request(geometry.width, geometry.height)

    def show(self):
        self._ensure_position()
        self.present()

    def toggle(self):
        if self.get_visible():
            self.hide()
        else:
            self.show()
