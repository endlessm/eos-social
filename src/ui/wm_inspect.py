import gobject
import wnck


class WM_Inspect_MixIn(object):


    CHECK_INTERVAL = 100
    def __init__(self):
        super(WM_Inspect_MixIn, self).__init__()
        gobject.timeout_add(self.CHECK_INTERVAL, self._check_active)

    def _check_active(self):
        active_name = self._get_active_window_name()
        if hasattr(self, '_active_win_callback'):
            try:
                self._active_win_callback(active_name)
            except:
                pass
        return True

    def _get_active_window_name(self):
        try:
            default = wnck.screen_get_default()
            window_list = default.get_windows()
            active_win = self._find_active(window_list)
            if active_win is not None:
                return active_win.get_name()
        except:
            pass
        return None

    def _find_active(self, window_list):
        if len(window_list) == 0:
            return None
        for win in window_list:
            if win.is_active():
                return win
        return None
