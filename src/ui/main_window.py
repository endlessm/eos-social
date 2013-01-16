import gtk
import gobject
import os
import pango
import cairo
from animations import WindowAnimator
from skinable_window import SkinableWindow
from wm_inspect import WM_Inspect_MixIn


class MainWindow(SkinableWindow, WM_Inspect_MixIn):


    DEFAULT_WINDOW_WIDTH = 400
    MINIMUM_WINDOW_WIDTH = 10
    ANIMATION_STEP = 20
    ANIMATION_TIME = 50
    def __init__(self):
        SkinableWindow.__init__(self, gtk.WINDOW_TOPLEVEL)
        WM_Inspect_MixIn.__init__(self)
        self.first_run = True
        self._last_show_state = None
        screen_height = gtk.gdk.screen_height()
        screen_width = gtk.gdk.screen_width()
        self.y_loc = 45
        self.height_loc = screen_height - self.y_loc - 38
        self.set_resizable(False)
        #self.set_size_request(self.MINIMUM_WINDOW_WIDTH, self.height_loc)
        self.set_size_request(self.DEFAULT_WINDOW_WIDTH, self.height_loc)
        self.stick() # this sticks on all desktops
        #self.set_keep_above(True)
        self.set_decorated(False)
        self.set_modal(True)
        self.set_skip_pager_hint(True)
        self.move(screen_width, self.y_loc)

        self.alloc_expanded = gtk.gdk.Rectangle(
          x=screen_width-self.DEFAULT_WINDOW_WIDTH, 
          y=self.y_loc, 
          width=self.DEFAULT_WINDOW_WIDTH, 
          height=self.height_loc
          )
        self.alloc_collapsed = gtk.gdk.Rectangle(
          x=screen_width, 
          y=self.y_loc, 
          width=self.MINIMUM_WINDOW_WIDTH, 
          height=self.height_loc
          )
        self.connect('delete-event', lambda w, e: True)
        self.set_role("eos-non-max")
        self.set_skip_taskbar_hint(True)

    def _active_win_callback(self, active_name):
        if active_name == 'Endless Social Bar':
            self._last_show_state = 'max'
            self._maximize()
        elif active_name == 'Endless OS Browser':
            self._last_show_state = 'max'
            self._maximize()
        else:
            if self._last_show_state is not None:
                self._minimize()
                self._last_show_state = None

    def _minimize(self):
        self._freez_on_set_focus = True
        self._frezz_on_visible = True
        self._last_show_state = 'min'
        def cb():
            self.iconify()
            self._frezz_on_visible = False
        self._hide_animation(lambda: cb())

    def _maximize(self):
        self._last_show_state = 'max'
        def cb():
            self._freez_on_set_focus = False
        top_level = self.get_toplevel()
        top_level_x, top_level_y = top_level.get_window().get_origin()
        pos_x = top_level_x + self.allocation.x
        if pos_x != self.alloc_expanded.x:
            self._show_animation(lambda: cb())

    def _show_animation(self, callback):
        start_alloc = gtk.gdk.Rectangle(
          x=self.alloc_collapsed.x, 
          y=self.alloc_collapsed.y, 
          width=self.alloc_collapsed.width, 
          height=self.alloc_collapsed.height
          )
        end_alloc = gtk.gdk.Rectangle(
          self.alloc_expanded.x, 
          self.alloc_expanded.y, 
          self.alloc_expanded.width, 
          self.alloc_expanded.height
          )
        anim = WindowAnimator(self, start_alloc, end_alloc, callback, 
          animation_step=self.ANIMATION_STEP, 
          animation_time=self.ANIMATION_TIME
          )
        gobject.timeout_add(anim.get_animation_time(), anim)

    def _hide_animation(self, callback):
        start_alloc = gtk.gdk.Rectangle(
          x=self.alloc_expanded.x, 
          y=self.alloc_expanded.y, 
          width=self.alloc_expanded.width, 
          height=self.alloc_expanded.height
          )
        end_alloc = gtk.gdk.Rectangle(
          self.alloc_collapsed.x, 
          self.alloc_collapsed.y, 
          self.alloc_collapsed.width, 
          self.alloc_collapsed.height
          )
        anim = WindowAnimator(self, start_alloc, end_alloc, callback, 
          animation_step=self.ANIMATION_STEP, 
          animation_time=self.ANIMATION_TIME
          )
        gobject.timeout_add(anim.get_animation_time(), anim)

    def show_delayed(self):
        if not self.first_run:
            return
        self.first_run = False
        def _callback():
            self._maximize()
            return False
        gobject.timeout_add(2000, _callback)



