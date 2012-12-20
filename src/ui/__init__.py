import gtk
import gobject
import os
import pango


class MainWindow(gtk.Window):


    DEFAULT_WINDOW_WIDTH = 400
    def __init__(self, transparent=False, dock=None):
        super(MainWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.image_path = None
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
        self.connect('expose-event', self._on_draw)

        position = self._get_position_by_dock(dock)
        if position is not None:
            self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
            self.show() # must call show() before property_change()
            self.window.property_change("_NET_WM_STRUT", "CARDINAL", 32, 
              gtk.gdk.PROP_MODE_REPLACE, position)
        else:
            self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)

    def _on_draw(self, widget, event):
        if os.path.isfile(self.image_path):
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file(self.image_path)
                pixbuf_scaled = pixbuf.scale_simple(event.area.width, event.area.height, gtk.gdk.INTERP_BILINEAR)
                widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf_scaled, 0, 0, 0,0)
                del pixbuf_scaled
                del pixbuf
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


class UserAvatar(gtk.EventBox):


    SIZE = {
        'user_avatar': (24, 24), 
        }

    def __init__(self):
        super(UserAvatar, self).__init__()
        self._user_avatar = gtk.Image()
        self._user_avatar.set_size_request(*self.SIZE['user_avatar'])
        self.add(self._user_avatar)

    def show(self):
        super(UserAvatar, self).show()
        self._user_avatar.show()

    def hide(self):
        self._user_avatar.hide()
        super(UserAvatar, self).hide()

    def set_avatar(self, image_path):
        if os.path.isfile(image_path):
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file(image_path)
                w, h = self.SIZE['user_avatar']
                pixbuf_scaled = pixbuf.scale_simple(w, h, gtk.gdk.INTERP_BILINEAR)
                del pixbuf
                self._user_avatar.set_from_pixbuf(pixbuf_scaled)
                del scaled_pixbuf
            except:
                pass


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

    IMG_PATH = '/usr/share/endlessm_social_bar/images/'

    LOC = {
        'post': (5, 12), 
        'chat': (100, 12), 
        'feed': (145, 12), 
        'settings': (220, 12), 
        'close': (345, 12), 
        'avatar': (370, 12), 
        }

    IMG = {
        'post': {'normal', 'publish_button_normal.png', }, 
        'chat': '', 
        'feed': '', 
        'settings': '', 
        'close': '', 
        'avatar': '', 
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
        #button = gtk.Button(title)
        button = SimpleButton()
        #button.connect('clicked', self._emit_action, button_name)
        button.connect('button-press-event', 
          lambda w, e: self._emit_action(w, button_name))
        button.set_size_request(width, height)
        self._buttons[button_name] = button
        return button

    def _get_button(self, button_name):
        button = self._buttons.get(button_name, None)
        return button

    def __init__(self, post_send_area, user_avatar):
        super(PostMessage, self).__init__()
        self.set_size_request(-1, self.COLLAPSED_HEIGHT)
        self._buttons = {}

        self.toolbar = gtk.Fixed()
        self.toolbar.set_size_request(-1, self.COLLAPSED_HEIGHT)

        self.post_wraper = post_send_area
        self.user_avatar = user_avatar

        self.toolbar.put(self.user_avatar, *self.LOC['avatar'])
        self.user_avatar.connect('button-press-event', 
          lambda w, e: self._emit_action(w, 'avatar'))

        self.toolbar_wraper = gtk.VBox()
        self.toolbar_wraper.pack_start(self.toolbar, False, False)
        self.toolbar_wraper.pack_start(self.post_wraper, True, True)

        ##self.add(self.toolbar)
        self.add(self.toolbar_wraper)

        #self.toolbar.put(self._create_button('post', title='post'), 
        #  *self.LOC['post'])

        post = SimpleButton()
        self.toolbar.put(post, *self.LOC['post'])
        post.connect('button-press-event', 
          lambda w, e: self._emit_action(w, 'post'))
        post.show_image(
          '/usr/share/endlessm_social_bar/images/publish_button_normal.png')
        post.set_image('click', 
          '/usr/share/endlessm_social_bar/images/publish_button_down.png')
        post.set_image('release', 
          '/usr/share/endlessm_social_bar/images/publish_button_normal.png')
        post.set_image('enter', 
          '/usr/share/endlessm_social_bar/images/publish_button_hover.png')
        post.set_image('leave', 
          '/usr/share/endlessm_social_bar/images/publish_button_normal.png')

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


class WelcomePanel(gtk.Alignment):


    __gsignals__ = {
        'welcome-panel-action': (
            gobject.SIGNAL_RUN_FIRST, 
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING, )
            ),
    }

    def _emit_action(self, widget, action):
        self.emit('welcome-panel-action', action)

    def __init__(self):
        super(WelcomePanel, self).__init__(xalign=0.5, yalign=0.5)
        self._container = gtk.VBox()
        self.add(self._container)
        self.welcome_text_h1 = gtk.Label()
        self.welcome_text_h1.set_markup(
          """<span foreground="white">Welcome!</span>""")
        self.welcome_text_h1.modify_font(pango.FontDescription("sans 16"))
        self.welcome_text_h2 = gtk.Label()
        self.welcome_text_h2.set_markup(
          """<span foreground="white">We've brought Facebook to your</span>""")
        self.welcome_text_h3 = gtk.Label()
        self.welcome_text_h3.set_markup(
          """<span foreground="white">desktop. Please Login below.</span>""")
        self.welcome_button = gtk.Button('Login')
        self.fb_button = SimpleButton()
        self.fb_button.set_size_request(128, 34)
        self.fb_button.set_image('leave', 
          '/usr/share/endlessm_social_bar/images/login_button_normal.png')
        self.fb_button.set_image('enter', 
          '/usr/share/endlessm_social_bar/images/login_button_hover.png')
        self.fb_button.show_image(
          '/usr/share/endlessm_social_bar/images/login_button_normal.png')
        self.fb_button.connect('button-press-event', 
          lambda w, e: self._emit_action(w, 'login'))

        self.fb_button.show()
        self.fb_button_wraper = gtk.Alignment(xalign=0.5, yalign=0.5)
        self.fb_button_wraper.add(self.fb_button)
        self.fb_button_wraper.show()

        self.welcome_button_wraper = gtk.Alignment(xalign=0.5, yalign=0.5)
        self.welcome_button_wraper.add(self.welcome_button)
        self.welcome_button.connect('button-press-event', 
          lambda w, e: self._emit_action(w, 'login'))
        self._container.pack_start(self.welcome_text_h1)
        self._container.pack_start(gtk.Label())
        self._container.pack_start(self.welcome_text_h2)
        self._container.pack_start(self.welcome_text_h3)
        #self._container.pack_start(self.welcome_button_wraper)
        self._container.pack_start(gtk.Label())
        self._container.pack_start(self.fb_button_wraper)


class MultiPanel(gtk.Alignment):


    def __init__(self):
        super(MultiPanel, self).__init__(xalign=0.0, yalign=0.0, xscale=1.0, 
          yscale=1.0)
        self._map = {}
        self._container = gtk.VBox()
        self.add(self._container)
        self._container.hide()
        self.hide()

    def add_panel(self, panel, panel_name):
        self._map[panel_name] = panel
        self._container.pack_start(panel, expand=True, fill=True, padding=0)
        panel.hide()

    def _show_panel(self, panel):
        for current_panel in self._map.values():
            if current_panel is panel:
                current_panel.show()
            else:
                current_panel.hide()

    def show_panel(self, panel_name):
        panel = self._map.get(panel_name, None)
        if panel is not None:
            self._show_panel(panel)

    def hide_all(self):
        for current_panel in self._map.values():
            current_panel.hide()


class SimpleButton(gtk.EventBox):


    def __init__(self):
        super(SimpleButton, self).__init__()
        #self.connect("expose-event", self._on_draw)
        self._image_map = {}
        self.set_visible_window(False)
        self.image = gtk.Image()
        self.add(self.image)
        self.connect('button-press-event', self._on_click)
        self.connect('button_release_event', self._on_release)
        self.connect('enter_notify_event', self._on_enter)
        self.connect('leave_notify_event', self._on_leave)
        self.set_events(gtk.gdk.EXPOSURE_MASK
                            | gtk.gdk.LEAVE_NOTIFY_MASK
                            | gtk.gdk.ENTER_NOTIFY_MASK
                            | gtk.gdk.BUTTON_PRESS_MASK
                            | gtk.gdk.BUTTON_RELEASE_MASK
                            )

    def set_image(self, image_name, image_file):
        self._image_map[image_name] = image_file

    def show_image(self, image_file):
        if image_file:
            self.image.set_from_file(image_file)

    def _on_click(self, w, e):
        self.show_image(self._image_map.get('click', None))

    def _on_release(self, w, e):
        self.show_image(self._image_map.get('release', None))

    def _on_enter(self, w, e):
        self.show_image(self._image_map.get('enter', None))

    def _on_leave(self, w, e):
        self.show_image(self._image_map.get('leave', None))


    #def _on_draw(self, widget, event):
    #    print 'draw'
















