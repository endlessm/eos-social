import gtk
import gobject
import os
import pango
import cairo
from skinable_window import SkinableWindow
from wm_inspect import WM_Inspect_MixIn


class WindowStateData(object):


    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and \
            (self.width == other.width) and (self.height == other.height)


class MainWindow(SkinableWindow, WM_Inspect_MixIn):


    def __init__(self, width=400, top_offset=0, bottom_offset=38):
        SkinableWindow.__init__(self, gtk.WINDOW_TOPLEVEL)
        WM_Inspect_MixIn.__init__(self)
        self._ignore_win_names = ()

        height = gtk.gdk.screen_height() - top_offset - bottom_offset
        self.show_state = WindowStateData(gtk.gdk.screen_width()-width, 
          top_offset, width, height)
        self.hide_state = WindowStateData(gtk.gdk.screen_width(), top_offset, 
          width, height)

        self.first_run = True
        self._last_show_state = None
        self.freeze_window = False

        self.connect('delete-event', lambda w, e: True)
        self._set_options()
        self.set_state(self.hide_state)

    def set_ignore_win_names(self, names):
        self._ignore_win_names = names

    def get_current_state(self):
        return self._get_current_state()

    def _get_current_state(self):
        try:
            top_level = self.get_toplevel()
            x, y = top_level.get_window().get_origin()
            w = self.allocation.width
            h = self.allocation.height
            return WindowStateData(x, y, w, h)
        except:
            pass
        return None

    def set_state(self, state):
        current_state = self._get_current_state()
        if current_state != state:
            self.move(state.x, state.y)
            self.set_size_request(state.width, state.height)

    def _set_options(self):
        self.set_resizable(False)
        self.set_role("eos-non-max")
        self.set_skip_taskbar_hint(True)
        self.stick() # this sticks on all desktops
        #self.set_keep_above(True)
        self.set_decorated(False)
        self.set_modal(True)
        self.set_skip_pager_hint(True)

    def _active_win_callback(self, active_name):
        if self.freeze_window:
            return
        if active_name in self._ignore_win_names:
            self._last_show_state = 'max'
            self.show()
        else:
            if self._last_show_state is not None:
                self.hide()
                self._last_show_state = None

    def freeze(self):
        self.freeze_window = True

    def unfreeze(self):
        self.freeze_window = False

    def show(self):
        self.set_state(self.show_state)

    def hide(self):
        self.set_state(self.hide_state)
        self.iconify()
