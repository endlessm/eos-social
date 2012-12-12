import gtk


class MainWindow(gtk.Window):


    DEFAULT_WINDOW_WIDTH = 400
    def __init__(self, transparent=False, dock=None):
        super(MainWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        screen_height = gtk.gdk.screen_height() - 80
        screen_width = gtk.gdk.screen_width()
        self.set_app_paintable(True)
        if transparent:
            self.set_colormap(win.get_screen().get_rgba_colormap())

        self.set_resizable(False)
        self.set_default_size(self.DEFAULT_WINDOW_WIDTH, screen_height)
        self.set_size_request(self.DEFAULT_WINDOW_WIDTH, screen_height)
        self.stick() # this sticks on all desktops
        self.set_keep_above(True)
        self.set_modal(True)
        self.set_skip_pager_hint(True)
        self.move(screen_width-self.DEFAULT_WINDOW_WIDTH, 0)

        position = self._get_position_by_dock(dock)
        if position is not None:
            self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
            self.show() # must call show() before property_change()
            self.window.property_change("_NET_WM_STRUT", "CARDINAL", 32, 
              gtk.gdk.PROP_MODE_REPLACE, position)
        else:
            self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)

    def _get_position_by_dock(self, dock):
        position = None
        if dock == 'right':
            position = [0, self.DEFAULT_WINDOW_WIDTH, 0, 0]
        elif dock == 'left':
            #TODO: make it dockable to left side
            pass
        else:
            pass
        return position


class SimplePopUp(gtk.Window):


    DEFAULT_WINDOW_WIDTH = 200
    DEFAULT_WINDOW_HEIGHT = 100

    def __init__(self, message_text=None):
        super(SimplePopUp, self).__init__()
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.set_default_size(self.DEFAULT_WINDOW_WIDTH, self.DEFAULT_WINDOW_HEIGHT)
        self._label = gtk.Label()
        self.add(self._label)
        self._message_text = message_text
        self.set_modal(True)

    def show(self):
        message_text = self._message_text or ''
        self._label.set_text(message_text)
        super(SimplePopUp, self).show_all()




