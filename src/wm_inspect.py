from gi.repository import GObject
from gi.repository import Wnck


class WM_Inspect_MixIn(object):


    def __init__(self):
        super(WM_Inspect_MixIn, self).__init__()

        self._screen = Wnck.Screen.get_default()
        self._screen.connect('active-window-changed', self._on_active_window_changed)

    def _on_active_window_changed(self, previous, data):
        active_window = self._screen.get_active_window()
        if not active_window:
            return
        if hasattr(self, '_active_win_callback'):
            self._active_win_callback(active_window.get_xid())
