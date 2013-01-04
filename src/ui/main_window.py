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
        self._last_show_state = None
        self._freez_on_set_focus = False
        self._frezz_on_visible = False
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

        self.init_alloc = gtk.gdk.Rectangle(
          x=screen_width-self.DEFAULT_WINDOW_WIDTH, 
          y=0, 
          width=self.DEFAULT_WINDOW_WIDTH, 
          height=screen_height
          )

        self.connect('notify::is-active', self._set_focus)
        self.connect('expose-event', self._on_draw)
        self.connect('delete-event', self._on_close)
        self.connect('visibility-notify-event', self._on_visible)
        #self.connect('window-state-event', self._on_state)

        self.set_role("eos-non-max")

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

    #def _on_state(self, widget, event):
    #    print '_on_state', self.get_property('visible')

    def _on_visible(self, widget, event):
        print '_on_visible'
        if not self._frezz_on_visible:
            print '..active'
            if self._last_show_state is None or self._last_show_state != 'max':
                self._maximize()
            else:
                print 'already max'

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
        print '_set_focus'
        if not self._freez_on_set_focus:
            print 'freez_sense', self._freez_on_set_focus
            if self.focus_out_active and not window.props.is_active:
                self._minimize()

    def collapse(self):
        self._minimize()

    def _minimize(self):
        print '_minimize'
        self._freez_on_set_focus = True
        self._frezz_on_visible = True
        self._last_show_state = 'min'
        def cb():
            print 'cb..'
            self.iconify()
            self._frezz_on_visible = False
        self._hide_animation(lambda: cb())

    def _maximize(self):
        print '_maximize'
        self._last_show_state = 'max'
        self._show_animation()
        self._freez_on_set_focus = False

    def _show_animation(self):
        print '_show_animation'
        print 'init_alloc', self.init_alloc
        self.move(self.init_alloc.x, self.init_alloc.y)
        self.set_size_request(self.init_alloc.width, self.init_alloc.height)



    def _hide_animation(self, callback):
        print '_hide_animation'
        start_alloc = gtk.gdk.Rectangle(self.init_alloc.x, self.init_alloc.y, 
          self.init_alloc.width, self.init_alloc.height)

        end_alloc = gtk.gdk.Rectangle(x=0, y=0, width=0, height=0)
        anim = dummy(self, start_alloc, end_alloc, callback)
        gobject.timeout_add(anim.ANIMATION_TIME, anim)

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



class dummy:
    ANIMATION_STEP = 10
    ANIMATION_TIME = 200
    MIN_WIDTH = 50
    def __init__(s, window, start_alloc, end_alloc, callback=None):
        s.window = window
        s.start_alloc = start_alloc
        s.end_alloc = end_alloc
        s.curr_alloc = gtk.gdk.Rectangle(start_alloc.x, start_alloc.y, 
          start_alloc.width, start_alloc.height)
        s.callback = callback

    def __call__(s):
        print '__call__'
        s.curr_alloc.x += s.ANIMATION_STEP
        s.curr_alloc.width -= s.ANIMATION_STEP
        if s.curr_alloc.width < s.MIN_WIDTH:
            print 'done'
            if s.callback is not None:
                try:
                    s.callback()
                except:
                    pass
            return False
        else:
            s.window.move(s.curr_alloc.x, s.curr_alloc.y)
            s.window.set_size_request(s.curr_alloc.width, s.curr_alloc.height)
            return True

