import gtk
import gobject
import os
import pango
import cairo
import gettext

from simple_button import SimpleButton
from main_window import MainWindow
from user_profile_menu import UserProfileMenu
from dialogs import SelectVideoDialog

gettext.install('eos-social', '/usr/share/locale', unicode=True, names=['ngettext'])

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


    __gsignals__ = {
        'user-profile-action': (
            gobject.SIGNAL_RUN_FIRST, 
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING, )
            ),
    }

    SIZE = {
        'user_avatar': (32, 33), 
        }

    def __init__(self, menu):
        super(UserAvatar, self).__init__()
        self._presenter = None
        self._avatar_expanded = False
        self._user_avatar = gtk.Image()
        self._user_avatar.set_size_request(*self.SIZE['user_avatar'])
        self.add(self._user_avatar)
        self.menu = menu
        self.menu.connect('user-profile-action', 
          lambda w, a: self.emit('user-profile-action', a))
        self.connect("enter-notify-event", self._on_enter)
        self.connect("leave-notify-event", self._on_leave)
        ##self.connect('button-press-event', self._on_click)

    def show(self):
        super(UserAvatar, self).show()
        self._user_avatar.show()

    def get_is_expanded(self):
        return self._avatar_expanded

    def set_is_expanded(self, value):
        self._avatar_expanded = value

    def hide(self):
        self._user_avatar.hide()
        super(UserAvatar, self).hide()

    def set_presenter(self, presenter):
        self._presenter = presenter
        self.set_avatar(self._presenter.get_no_picture_file_path())

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

    def _on_click(self, widget, event):
        top_level = self.get_toplevel()
        top_level_x, top_level_y = top_level.get_window().get_origin()
        pos_x = top_level_x + self.allocation.x
        pos_y = top_level_y + self.allocation.y + self.allocation.height
        # move to end of user profile
        pos_x = pos_x + self.allocation.width
        state = self._presenter.get_logout_on_shutdown_active()
        self.menu.set_logout_on_shutdown_active(state)
        self.menu.show(pos_x, pos_y)
        self.menu.run()
    
    def _on_enter(self, widget, event):
        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))

    def _on_leave(self, widget, event):
        widget.window.set_cursor(None)

class PostMessageSendArea(gtk.Alignment):


    SIZE = {
        'fb': (32, 32), 
        'send': (20, 21), 
        'cancel': (20, 21), 
        'image_upload': (20, 21), 
        'video_upload': (20, 21), 
        }

    IMG = {
        # normal, click, release, enter, leave
        'send': (
          'send_button_normal.png', 
          'send_button_down.png', 
          'send_button_normal.png', 
          'send_button_hover.png', 
          'send_button_normal.png', 
          ), 
        'cancel': (
          'cancel_button_normal.png', 
          'cancel_button_down.png', 
          'cancel_button_normal.png', 
          'cancel_button_hover.png', 
          'cancel_button_normal.png', 
          ), 
        }

    IMG_PATH = '/usr/share/eos-social/images/'
    def _img(cls, key):
        images = cls.IMG[key]
        return [cls.IMG_PATH + img for img in images]

    DEFAULT_TEXT = _('Type status here')

    __gsignals__ = {
        'post-panel-action': (
            gobject.SIGNAL_RUN_FIRST, 
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING, )
            ),
    }

    def _emit_action(self, widget, action):
        self.emit('post-panel-action', action)

    def _make_button(self, button_name, button, width=40, height=20):
        width, height = self.SIZE[button_name]
        button.connect('button-press-event', 
          lambda w, e: self._emit_action(w, button_name))
        button.set_size_request(width, height)
        self._buttons[button_name] = button
        return button

    def _get_button(self, name):
        return self._buttons.get(name, None)

    def enable_posting(self):
        button = self._get_button('send')
        button.set_sensitive(True)

    def disable_posting(self):
        button = self._get_button('send')
        button.set_sensitive(False)

    def _skin_it(self, button_name, button):
        images = self._img(button_name)
        button.show_image(images[0])
        button.set_image('click', images[1])
        button.set_image('release', images[2])
        button.set_image('enter', images[3])
        button.set_image('leave', images[4])

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
        self.text_buffer = self.text_area.get_buffer()
        self.text_buffer.set_text(self.DEFAULT_TEXT)
        self.text_buffer.connect('changed', self._text_changed)
        self.text_area.connect('focus-in-event', self._focus_in)
        self.text_area.connect('focus-out-event', self._focus_out)
        self.text_area.set_left_margin(5)
        self.text_area.set_right_margin(5)
        self.text_area.set_pixels_inside_wrap(3)
        self.text_area.set_pixels_below_lines(3)
        self.text_area.set_pixels_above_lines(3)

        self.text_area_wraper = gtk.HBox(True)
        self.text_area_wraper.pack_start(self.text_area, True, True, 10)

        send = self._make_button('send', SimpleButton())
        send.connect("enter-notify-event", self._on_enter)
        send.connect("leave-notify-event", self._on_leave)
        self._skin_it('send', send)

        cancel = self._make_button('cancel', SimpleButton())
        cancel.connect("enter-notify-event", self._on_enter)
        cancel.connect("leave-notify-event", self._on_leave)
        self._skin_it('cancel', cancel)

        image_upload = self._make_button('image_upload', gtk.Button('image_upload'))
        video_upload = self._make_button('video_upload', gtk.Button('video_upload'))

        self.post_toolbar = gtk.HBox()
        self.post_toolbar.pack_end(send, False, False, 5)
        self.post_toolbar.pack_end(cancel, False, False, 5)
        self.post_toolbar.pack_start(image_upload, False, False, 5)
        self.post_toolbar.pack_start(video_upload, False, False, 5)

        self.post_wraper = gtk.VBox()
        self.post_wraper.pack_start(self.text_area_wraper, True, True)
        self.post_wraper.pack_end(self.post_toolbar, False, False, 3)

        self.add(self.post_wraper)

    def get_post_message(self):
        text = self._get_text()
        if text == '' or text == self.DEFAULT_TEXT:
            return None
        return text

    def _text_changed(self, textbuffer):
        self._emit_action(self, 'post_msg_changed')

    def _get_text(self):
        text_buffer = self.text_area.get_buffer()
        start, end = text_buffer.get_bounds()
        #text = text_buffer.get_slice(start, end, False)
        return text_buffer.get_text(start, end, False)

    def get_text_area(self):
        return self.text_area

    def clear_text(self, force=False):
        if force or self._get_text() == self.DEFAULT_TEXT:
            self.text_area.get_buffer().set_text('')

    def set_default_text(self):
        self.text_area.get_buffer().set_text(self.DEFAULT_TEXT)

    def show(self):
        super(PostMessageSendArea, self).show()
        self.post_toolbar.show()

    def hide(self):
        self.post_toolbar.hide()
        super(PostMessageSendArea, self).hide()
    
    def _on_enter(self, widget, event):
        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        
    def _on_leave(self, widget, event):
        widget.window.set_cursor(None)


class PostMessage(gtk.Alignment):

    ANIMATION_STEP = 40
    COLLAPSED_HEIGHT = 70 + ANIMATION_STEP
    EXPANDED_HEIGHT = 160 - ANIMATION_STEP

    IMG_PATH = '/usr/share/eos-social/images/'

    LOC = {
        'post': (10, 15), 
        'chat': (100, 15), 
        'feed': (145, 15), 
        'settings': (220, 15), 
        'avatar': (334, 15), 
        'close': (375, 5), 
        'user_name': (200, 15), 
        'logout': (200, 30), 
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
        'post': (32, 33), 
        'chat': (45, 26), 
        'feed': (45, 26), 
        'settings': (65, 26), 
        'close': (20, 21), 
        'avatar': (32, 33), 
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

    def __init__(self, post_send_area, user_avatar, user_name, logout):
        super(PostMessage, self).__init__()
        self.set_size_request(-1, self.COLLAPSED_HEIGHT)
        self._buttons = {}
        self.last_click = None

        self.toolbar = gtk.Fixed()
        self.toolbar.set_size_request(-1, self.COLLAPSED_HEIGHT-self.ANIMATION_STEP)

        self.post_wraper = post_send_area
        self.user_avatar = user_avatar
        self.user_name = user_name
        self.logout = logout

        self.connect('hierarchy-changed', self._on_parent_change)

        self.user_avatar.connect('button_press_event', self._on_click)
        self.user_name.connect('button_press_event', self._on_click)
        self.logout.connect('button_press_event', self._on_click)

        self.toolbar.put(self.user_avatar, *self.LOC['avatar'])
        self.toolbar.put(self.user_name, *self.LOC['user_name'])
        self.toolbar.put(self.logout, *self.LOC['logout'])

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
        post.connect("enter-notify-event", self._on_enter)
        post.connect("leave-notify-event", self._on_leave)
        post.show_image(
          '/usr/share/eos-social/images/publish_button_normal.png')
        post.set_image('click', 
          '/usr/share/eos-social/images/publish_button_down.png')
        post.set_image('release', 
          '/usr/share/eos-social/images/publish_button_normal.png')
        post.set_image('enter', 
          '/usr/share/eos-social/images/publish_button_hover.png')
        post.set_image('leave', 
          '/usr/share/eos-social/images/publish_button_normal.png')

        close = SimpleButton()
        self.toolbar.put(close, *self.LOC['close'])
        close.connect('button-press-event', 
          lambda w, e: self._emit_action(w, 'close'))
        close.connect("enter-notify-event", self._on_enter)
        close.connect("leave-notify-event", self._on_leave)
        close.show_image(
          '/usr/share/eos-social/images/cancel_button_normal.png')
        close.set_image('click', 
          '/usr/share/eos-social/images/images/cancel_button_down.png')
        close.set_image('release', 
          '/usr/share/eos-social/images/images/cancel_button_normal.png')
        close.set_image('enter', 
          '/usr/share/eos-social/images/cancel_button_hover.png')
        close.set_image('leave', 
          '/usr/share/eos-social/images/cancel_button_normal.png')

        self.collapse_text_field()

    def _on_parent_change(self, widget, previous_toplevel):
        root_win = self.get_toplevel()
        root_win.connect('button_press_event', self._on_click)
        root_win.set_events(gtk.gdk.BUTTON_PRESS_MASK)

    def _on_click(self, widget, event):
        if self.last_click is None or self.last_click is widget:
            self.user_avatar.set_is_expanded(False)
            self.user_name.hide()
            self.logout.hide()
        self.last_click = widget

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
            calc_h = self.allocation.height+self.ANIMATION_STEP
            self.set_size_request(-1, calc_h)
            not_done = calc_h < self.EXPANDED_HEIGHT
            if not_done:
                self.post_wraper.hide()
                #self.text_area.hide()
            else:
                self.post_wraper.show()
                #self.text_area.show()
            return not_done
        gobject.timeout_add(1, animate)

    def collapse_text_field(self):
        self.post_wraper.hide()
        def animate():
            h = self.allocation.height-self.ANIMATION_STEP
            h = h if h > 0 else 0
            self.set_size_request(-1, h)
            not_done = self.allocation.height > self.COLLAPSED_HEIGHT
            if not not_done:
                self.post_wraper.hide()
            return not_done
        gobject.timeout_add(1, animate)

    def toggle_text_field(self):
        if self.allocation.height < self.EXPANDED_HEIGHT:
            self.expand_text_field()
        else:
            self.collapse_text_field()
    
    def _on_enter(self, widget, event):
        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        
    def _on_leave(self, widget, event):
        widget.window.set_cursor(None)
    

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
          """<span foreground="white">""" + _('Welcome!') + """</span>""")
        self.welcome_text_h1.modify_font(pango.FontDescription("sans 16"))
        self.welcome_text_h2 = gtk.Label()
        self.welcome_text_h2.set_markup(
          """<span foreground="white">""" + _("We've brought Facebook to your") + """</span>""")
        self.welcome_text_h3 = gtk.Label()
        self.welcome_text_h3.set_markup(
          """<span foreground="white">""" + _('desktop. Please Login below.') + """</span>""")
        self.welcome_button = gtk.Button(_('Login'))
        #self.fb_button = SimpleButton()
        self.fb_button = LabelButton()
        self.fb_button.set_text(_('connect'), x=50, y=30)
        #self.fb_button.set_size_request(128, 34)
        self.fb_button.set_size_request(144, 50)
        self.fb_button.set_image('leave', 
          '/usr/share/eos-social/images/login_button_normal.png')
        self.fb_button.set_image('enter', 
          '/usr/share/eos-social/images/login_button_hover.png')
        self.fb_button.show_image(
          '/usr/share/eos-social/images/login_button_normal.png')
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


class LabelButton(gtk.EventBox):


    def __init__(self):
        super(LabelButton, self).__init__()
        self._image_map = {}
        self._text_x_offset = 0
        self._text_y_offset = 0
        self._text = ''
        self.set_visible_window(False)
        self.image_path = None
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
        self.connect('expose-event', self._on_draw)

    def _on_draw(self, widget, event):
        cr = self.window.cairo_create()
        self._draw_image(cr, event)
        cr.set_source_rgb(0.9, 0.9, 0.9)
        cr.select_font_face("sans", cairo.FONT_SLANT_NORMAL, 
          cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(16)
        #cr.move_to(self.allocation.x, self.allocation.y)
        x = event.area.x + self._text_x_offset
        y = event.area.y + self._text_y_offset
        cr.move_to(x, y)
        cr.show_text(self._text)

    def _draw_image(self, cr, event):
        if os.path.isfile(self.image_path):
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file(self.image_path)
                pixbuf_scaled = pixbuf.scale_simple(event.area.width, event.area.height, gtk.gdk.INTERP_BILINEAR)
                cr.set_source_pixbuf(pixbuf, event.area.x, event.area.y)
                del pixbuf_scaled
                del pixbuf
                cr.paint()
            except:
                pass

    def set_text(self, text, x=0, y=0):
        self._text = text
        self._text_x_offset = x
        self._text_y_offset = y

    def set_image(self, image_name, image_file):
        self._image_map[image_name] = image_file

    def show_image(self, image_file):
        if image_file:
            self.image_path = image_file
            self.queue_draw()

    def _on_click(self, w, e):
        self.show_image(self._image_map.get('click', None))

    def _on_release(self, w, e):
        self.show_image(self._image_map.get('release', None))

    def _on_enter(self, w, e):
        self.show_image(self._image_map.get('enter', None))

    def _on_leave(self, w, e):
        self.show_image(self._image_map.get('leave', None))


class LogoutLabel(gtk.EventBox):


    __gsignals__ = {
        'logout-label-action': (
            gobject.SIGNAL_RUN_FIRST, 
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING, )
            ),
    }

    def _emit_action(self, widget, action):
        self.emit('logout-label-action', action)

    def __init__(self, text):
        super(LogoutLabel, self).__init__()
        self.text = text
        self.label = gtk.Label(self.text)
        self.add(self.label)
        self.set_visible_window(False)
        self.label.set_markup(
          """<span foreground="gray">""" + self.text + """</span>""")
        self.set_events(gtk.gdk.EXPOSURE_MASK
                            | gtk.gdk.LEAVE_NOTIFY_MASK
                            | gtk.gdk.ENTER_NOTIFY_MASK
                            | gtk.gdk.BUTTON_PRESS_MASK
                            | gtk.gdk.BUTTON_RELEASE_MASK
                            )
        self.connect("button_release_event", 
          lambda w, e: self._emit_action(w, 'logout'))
        self.connect('button-press-event', self._on_click)
        self.connect('button_release_event', self._on_release)
        self.connect('enter_notify_event', self._on_enter)
        self.connect('leave_notify_event', self._on_leave)

    def _on_click(self, w, e):
        self.label.set_markup(
          """<span foreground="#880000">""" + self.text + """</span>""")

    def _on_release(self, w, e):
        self.label.set_markup(
          """<span foreground="gray">""" + self.text + """</span>""")

    def _on_enter(self, w, e):
        self.label.set_markup(
          """<span foreground="#FF0000">""" + self.text + """</span>""")

    def _on_leave(self, w, e):
        self.label.set_markup(
          """<span foreground="gray">""" + self.text + """</span>""")


class UserNameLabel(gtk.EventBox):


    __gsignals__ = {
        'user-name-action': (
            gobject.SIGNAL_RUN_FIRST, 
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING, )
            ),
    }

    def _emit_action(self, widget, action):
        self.emit('user-name-action', action)

    def __init__(self, text):
        super(UserNameLabel, self).__init__()
        self.label = gtk.Label(text)
        self.add(self.label)
        self.set_visible_window(False)
        self.label.set_markup(
          """<span foreground="white">""" + text + """</span>""")
        self.set_events(gtk.gdk.EXPOSURE_MASK
                            | gtk.gdk.LEAVE_NOTIFY_MASK
                            | gtk.gdk.ENTER_NOTIFY_MASK
                            | gtk.gdk.BUTTON_PRESS_MASK
                            | gtk.gdk.BUTTON_RELEASE_MASK
                            )
        self.connect("button-press-event", 
          lambda w, e: self._emit_action(w, 'user-name'))

    def set_text(self, text):
        self.label.set_markup(
          """<span foreground="white">""" + text + """</span>""")




















