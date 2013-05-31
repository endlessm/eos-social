import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import signal
from social_bar_view import SocialBarView


class SocialBarDbus(dbus.service.Object):
    DBusGMainLoop(set_as_default=True)

    BUS_NAME = 'com.endlessm.SocialBar'
    BUS_PATH = '/com/endlessm/SocialBar'
    BUS_IFACE = 'com.endlessm.SocialBar'

    def __init__(self):
        bus_name = dbus.service.BusName(SocialBarDbus.BUS_NAME, bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, SocialBarDbus.BUS_PATH)
 
    @dbus.service.method(BUS_IFACE)
    def restore(self):
        self.view.slide_in()

    @dbus.service.method(BUS_IFACE)
    def toggle(self):
        self.view.toggle()

    @classmethod
    def is_running(self):
        app_name = dbus.SessionBus().request_name(SocialBarDbus.BUS_NAME)
        return app_name != dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER

    def run(self):
        self.view = SocialBarView()
        self.view.main()

def main():
    running = False
    try:
        running = SocialBarDbus.is_running()
    except:
        pass
    if running:
        bus = dbus.SessionBus()
        social_bar = bus.get_object(SocialBarDbus.BUS_NAME, SocialBarDbus.BUS_PATH)
        restore = social_bar.get_dbus_method('restore', SocialBarDbus.BUS_IFACE)
        restore()
    else:
        app = SocialBarDbus()
        # FIXME: Get rid of the following line which has the only purpose of
        # working around Ctrl+C not exiting Gtk applications from bug 622084.
        # https://bugzilla.gnome.org/show_bug.cgi?id=622084
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app.run()

