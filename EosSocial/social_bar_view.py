
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import WebKit

ALT = '<Alt>'

class SocialBarView(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,
                            type=Gtk.WindowType.TOPLEVEL,
                            decorated=False,
                            modal=True,
                            resizable=False,
                            skip_pager_hint=True,
                            skip_taskbar_hint=True)

        self.connect('focus-out-event', self._on_focus_out)
        self.connect('destroy', self._destroy)

        # stick on all desktops
        self.stick()
        # do not destroy on delete event
        self.connect('delete-event', lambda w, e: self.hide_on_delete())

        # update position when workarea changes
        screen = Gdk.Screen.get_default()
        screen.connect('monitors-changed', self._on_monitors_changed)

        self._create()

    def create_shortcuts(self, accelgroup=Gtk.AccelGroup()):
        for hotkey, modifier, callback in self._shortcuts:
            key, modifier = Gtk.accelerator_parse(modifier + hotkey)
            accelgroup.connect(key, modifier, Gtk.AccelFlags.VISIBLE, callback)
        self.add_accel_group(accelgroup)

    def _create(self):
        self._browser = WebKit.WebView()
        self._shortcuts = [('Left', ALT, lambda a, widget, c, m: self._browser.go_back()),
                           ('Right', ALT, lambda a, widget, c, m: self._browser.go_forward())]
        self.create_shortcuts()

        self.main_container = Gtk.ScrolledWindow()
        self.main_container.add(self._browser)

        self.add(self.main_container)
        self.show_all()
        self.hide()

        self._browser.load_uri('http://m.facebook.com')

    def _should_hide_on_focus_out(self, event):
        # When an event pops up and takes a grab, we get
        # a focus out event that we should ignore. Check
        # if Gtk thinks there's a grab, and if so, don't
        # hide.
        if Gtk.grab_get_current() is not None:
            return False

        return True

    def _on_focus_out(self, window, event):
        if self._should_hide_on_focus_out(event):
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

    def _destroy(self, *args):
        Gtk.main_quit()

    def main(self):
        GObject.threads_init()
        Gtk.main()
