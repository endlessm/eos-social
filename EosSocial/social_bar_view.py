
from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import WebKit

ALT = '<Alt>'
ANIM_TIME = (500 * 1000) # half a second

class FrameClockAnimator(object):
    def __init__(self, widget, duration):
        self._widget = widget
        self._tick_id = 0
        self._start_time = 0
        self._start_value = None
        self._end_value = None
        self._duration = float(duration)

    def start(self, end_value):
        if self._tick_id:
            return

        self._tick_id = self._widget.add_tick_callback(self._on_frame_tick, None)
        self._start_time = self._widget.get_frame_clock().get_frame_time()
        self._start_value = self._get_initial_value()
        self._end_value = end_value

    def stop(self):
        if not self._tick_id:
            return

        self._widget.remove_tick_callback(self._tick_id)

    # Robert Penner's easeOutQuint
    def _ease_time(self, t):
        p = t - 1
        return -1 * (p * p * p * p - 1)

    def _on_frame_tick(self, widget, frame_clock, user_data):
        t = (frame_clock.get_frame_time() - self._start_time) / self._duration
        if t > 1.0:
            self._tick_id = 0
            return False

        t = self._ease_time(t)
        new_value = self._start_value + (self._end_value - self._start_value) * t
        self.set_value(new_value)
        return True

class SocialBarSlider(FrameClockAnimator):
    def _get_initial_value(self):
        old_x, old_y = self._widget.get_position()
        return old_x

    def set_value(self, new_x):
        old_x, old_y = self._widget.get_position()
        self._widget.move(new_x, old_y)

class SocialBarView(Gtk.Window):
    def __init__(self):
        self.showing = False

        Gtk.Window.__init__(self,
                            type=Gtk.WindowType.TOPLEVEL,
                            type_hint=Gdk.WindowTypeHint.DOCK)

        self.connect('focus-out-event', self._on_focus_out)
        self.connect('destroy', self._destroy)

        # do not destroy on delete event
        self.connect('delete-event', lambda w, e: self.hide_on_delete())

        # update position when workarea changes
        screen = Gdk.Screen.get_default()
        screen.connect('monitors-changed', self._on_monitors_changed)

        self._animator = SocialBarSlider(self, ANIM_TIME)

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
        self._update_non_x_geometry()
        self._animator.set_value(self._get_final_x())
        self.show_all()

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
            self.slide_out()

    def _on_monitors_changed(self, screen, data):
        self._animator.stop()
        if self.showing:
            self._update_non_x_geometry()
            self._animator.set_value(self._get_final_x())

    def _get_workarea(self):
        screen = Gdk.Screen.get_default()
        monitor = screen.get_primary_monitor()
        return screen.get_monitor_workarea(monitor)

    def _get_final_x(self):
        width, height = self.get_size()
        workarea = self._get_workarea()
        x = workarea.width
        if self.showing:
            x -= width
        return x

    def _update_non_x_geometry(self):
        workarea = self._get_workarea()
        y = workarea.y
        width = workarea.width / 3
        height = workarea.height

        self.move(0, y)
        self.set_size_request(width, height)

    def slide_in(self):
        self.showing = True
        self._animator.start(self._get_final_x())

    def slide_out(self):
        self.showing = False
        self._animator.start(self._get_final_x())

    def toggle(self):
        if self.showing:
            self.slide_out()
        else:
            self.slide_in()

    def _destroy(self, *args):
        Gtk.main_quit()

    def main(self):
        GObject.threads_init()
        Gtk.main()
