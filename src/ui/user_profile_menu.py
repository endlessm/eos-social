import gtk
import gobject


class UserProfileMenu(gtk.Dialog):


    __gsignals__ = {
        'user-profile-action': (
            gobject.SIGNAL_RUN_FIRST, 
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING, )
            ),
    }

    def __init__(self, presenter):
        super(UserProfileMenu, self).__init__()
        self._fired_option = None
        self._presenter = presenter
        super(UserProfileMenu, self).set_decorated(False)
        super(UserProfileMenu, self).set_keep_above(True)
        super(UserProfileMenu, self).set_modal(True)
        super(UserProfileMenu, self).vbox.set_border_width(5)
        self.btn_user_profile = gtk.Button('User Profile')
        self.btn_user_profile.connect('clicked', self._on_click)
        self.btn_logout = gtk.Button('Logout')
        self.btn_logout.connect('clicked', self._on_click)
        self.logout_on_shutdown = gtk.CheckButton(label='Logout on Shutdown', use_underline=True)
        self.logout_on_shutdown.connect('clicked', self._on_click)
        self.connect('focus-out-event', lambda w, e: self.hide())
        super(UserProfileMenu, self).action_area.pack_start(self.logout_on_shutdown, padding = 3)
        super(UserProfileMenu, self).vbox.pack_start(self.btn_user_profile)
        super(UserProfileMenu, self).vbox.pack_start(self.btn_logout)

    def show(self, x, y):
        self._fired_option = None
        self.show_all()
        self.move(x - self.allocation.width, y)

    def get_logout_on_shutdown_active(self):
        return self.logout_on_shutdown.get_active()

    def set_logout_on_shutdown_active(self, state):
        self.logout_on_shutdown.set_active(state)

    def _on_click(self, widget):
        if widget == self.btn_user_profile:
            self._fired_option = 'user_profile'
        elif widget == self.btn_logout:
            self._fired_option = 'logout'
        elif widget == self.logout_on_shutdown:
            if self.get_logout_on_shutdown_active():
                self._fired_option = 'logout_on_shutdown_active'
            else:
                self._fired_option = 'logout_on_shutdown_inactive'
        self.hide()
        self.emit('user-profile-action', self._fired_option)


