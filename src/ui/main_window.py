import gtk
import gobject
import os
import pango
import cairo


class MainWindow(gtk.Window):


    DEFAULT_WINDOW_WIDTH = 400
    def __init__(self, transparent=False, dock=None):
        super(MainWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.image_path = None
        self.focus_out_active = True
        self.is_minimized = False
        screen_height = gtk.gdk.screen_height()
        screen_width = gtk.gdk.screen_width()
        self.set_app_paintable(True)
        if transparent:
            self.set_colormap(self.get_screen().get_rgba_colormap())

        self.set_resizable(False)
        self.set_default_size(self.DEFAULT_WINDOW_WIDTH, screen_height)
        self.set_size_request(self.DEFAULT_WINDOW_WIDTH, screen_height)
        self.stick() # this sticks on all desktops
        #self.set_keep_above(True)
        self.set_decorated(False)
        self.set_modal(True)
        self.set_skip_pager_hint(True)
        self.move(screen_width-self.DEFAULT_WINDOW_WIDTH, 0)
        self.connect("window-state-event", self.on_window_state_event)
        self.connect('notify::is-active', self._set_focus)
        self.connect('expose-event', self._on_draw)
        self.connect('delete-event', self._on_close)

        self.set_role("eos-non-max")
        self.set_skip_taskbar_hint(True)

        position = self._get_position_by_dock(dock)
        if position is not None:
            self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
            self.show() # must call show() before property_change()
            self.window.property_change("_NET_WM_STRUT", "CARDINAL", 32,
              gtk.gdk.PROP_MODE_REPLACE, position)
        else:
            #self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
            self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)

    def _on_close(self, widget, event):
        return True

    def set_focus_out_active(self, value):
        if value:
            self.get_focus()
            def activate_later():
                self.focus_out_active = True
                return False
            gobject.timeout_add(2000, activate_later)
        else:
            self.focus_out_active = False

    def _set_focus(self, window, gparam_boolean):
        if self.focus_out_active and not window.props.is_active and not self.is_minimized:
            window.iconify()

    def _on_draw(self, widget, event):
        if os.path.isfile(self.image_path):
            try:
                cr = widget.window.cairo_create()
                pixbuf = gtk.gdk.pixbuf_new_from_file(self.image_path)
                pixbuf_scaled = pixbuf.scale_simple(event.area.width, event.area.height, gtk.gdk.INTERP_BILINEAR)
                #widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf_scaled, 0, 0, 0,0)
                cr.set_source_pixbuf(pixbuf, 0, 0)
                del pixbuf_scaled
                del pixbuf
                cr.paint()
            except:
                pass

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

    def set_background_image(self, image_path):
        self.image_path = image_path
    
    def on_window_state_event(self, widget, event, data=None):
        if event.changed_mask & gtk.gdk.WINDOW_STATE_ICONIFIED:
            if event.new_window_state & gtk.gdk.WINDOW_STATE_ICONIFIED:
                self.is_minimized = True
            else:
                self.is_minimized = False

