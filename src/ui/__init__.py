import gtk
import gobject


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
        #self.set_keep_above(True)
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


class PostMessageSendArea(gtk.Alignment):


    SIZE = {
        'fb': (32, 32), 
        'send': (46, 32), 
        'cancel': (32, 32), 
        }

    DEFAULT_TEXT = 'Type status here'

    __gsignals__ = {
        'post-panel-action': (
            gobject.SIGNAL_RUN_FIRST, 
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING, )
            ),
    }

    def _emit_action(self, widget, action):
        self.emit('post-panel-action', action)

    def _create_button(self, button_name, width=40, height=20, title=''):
        width, height = self.SIZE[button_name]
        button = gtk.Button(title)
        button.connect('clicked', self._emit_action, button_name)
        button.set_size_request(width, height)
        self._buttons[button_name] = button
        return button

    def _focus_in(self, widget, event):
        self.clear_text()

    def _focus_out(self, widget, event):
        ##self.text_area.get_buffer().set_text('Type status here')
        pass

    def __init__(self):
        super(PostMessageSendArea, self).__init__()
        self._buttons = {}
        self.set_size_request(400, 100)
        self.text_area = gtk.TextView()
        self.text_area.set_editable(True)

        self.text_area.set_size_request(400, 100)
        ##self.text_area.set_size_request(380, self.COLLAPSED_HEIGHT) #390
        self.text_area.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.text_area.get_buffer().set_text(self.DEFAULT_TEXT)
        self.text_area.connect('focus-in-event', self._focus_in)
        self.text_area.connect('focus-out-event', self._focus_out)

        self.text_area_wraper = gtk.HBox(True)
        self.text_area_wraper.pack_start(self.text_area, True, True, 10)

        self.post_toolbar = gtk.HBox()
        self.post_toolbar.pack_end(self._create_button('cancel', title='x'), False, False, 10)
        self.post_toolbar.pack_end(self._create_button('send', title='send'), False, False, 10)

        self.post_wraper = gtk.VBox()
        self.post_wraper.pack_start(self.text_area_wraper, True, True)
        self.post_wraper.pack_end(self.post_toolbar, False, False, 3)

        self.add(self.post_wraper)

    def get_post_message(self):
        text_buffer = self.text_area.get_buffer()
        start, end = text_buffer.get_bounds()
        #text = text_buffer.get_slice(start, end, False)
        text = text_buffer.get_text(start, end, False)
        if text == '' or text == self.DEFAULT_TEXT:
            return None
        return text

    def get_text_area(self):
        return self.text_area

    def clear_text(self):
        self.text_area.get_buffer().set_text('')

    def set_default_text(self):
        self.text_area.get_buffer().set_text(self.DEFAULT_TEXT)

    def show(self):
        super(PostMessageSendArea, self).show()
        self.post_toolbar.show()

    def hide(self):
        self.post_toolbar.hide()
        super(PostMessageSendArea, self).hide()



class PostMessage(gtk.Alignment):

    COLLAPSED_HEIGHT = 50
    EXPANDED_HEIGHT = 150

    LOC = {
        'post': (5, 12), 
        'chat': (100, 12), 
        'feed': (145, 12), 
        'settings': (220, 12), 
        'close': (345, 12), 
        }

    SIZE = {
        'post': (45, 26), 
        'chat': (45, 26), 
        'feed': (45, 26), 
        'settings': (65, 26), 
        'close': (48, 26),  
        }

    __gsignals__ = {
        'post-panel-action': (
            gobject.SIGNAL_RUN_FIRST, 
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING, )
            ),
    }

    def _emit_action(self, widget, action):
        self.emit('post-panel-action', action)

    def _create_button(self, button_name, width=40, height=20, title=''):
        width, height = self.SIZE[button_name]
        button = gtk.Button(title)
        button.connect('clicked', self._emit_action, button_name)
        button.set_size_request(width, height)
        self._buttons[button_name] = button
        return button

    def _get_button(self, button_name):
        button = self._buttons.get(button_name, None)
        return button

    def __init__(self, post_send_area):
        super(PostMessage, self).__init__()
        self.set_size_request(-1, self.COLLAPSED_HEIGHT)
        self._buttons = {}

        self.toolbar = gtk.Fixed()
        self.toolbar.set_size_request(-1, self.COLLAPSED_HEIGHT)

        self.post_wraper = post_send_area

        self.toolbar_wraper = gtk.VBox()
        self.toolbar_wraper.pack_start(self.toolbar, False, False)
        self.toolbar_wraper.pack_start(self.post_wraper, True, True)

        ##self.add(self.toolbar)
        self.add(self.toolbar_wraper)

        self.toolbar.put(self._create_button('post', title='post'), 
          *self.LOC['post'])
        self.toolbar.put(self._create_button('close', title='close'), 
          *self.LOC['close'])

        self.collapse_text_field()

    def show(self):
        self.toolbar.show()
        ##self.text_area.hide()
        self.post_wraper.get_text_area().hide()
        super(PostMessage, self).show()

    def hide(self):
        super(PostMessage, self).hide()
        self.toolbar.hide()

    def expand_text_field(self):
        def animate():
            self.set_size_request(-1, self.allocation.height+10)
            not_done = self.allocation.height < self.EXPANDED_HEIGHT
            if not_done:
                self.post_wraper.hide()
                #self.text_area.hide()
            else:
                self.post_wraper.show()
                #self.text_area.show()
            return not_done
        gobject.timeout_add(2, animate)

    def collapse_text_field(self):
        self.post_wraper.hide()
        def animate():
            h = self.allocation.height-10
            h = h if h > 0 else 0
            self.set_size_request(-1, h)
            not_done = self.allocation.height > self.COLLAPSED_HEIGHT
            if not not_done:
                self.post_wraper.hide()
            return not_done
        gobject.timeout_add(2, animate)

    def toggle_text_field(self):
        if self.allocation.height < self.EXPANDED_HEIGHT:
            self.expand_text_field()
        else:
            self.collapse_text_field()





