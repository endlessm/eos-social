#!/usr/bin/env python
from social_bar_view import SocialBarView
from util.single_instance import DBusSingleAppInstance
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import subprocess
import signal
 
class SocialBarDbus(dbus.service.Object):
    DBusGMainLoop(set_as_default=True)
    def __init__(self):
        bus_name = dbus.service.BusName('org.social_bar.view', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/social_bar/view')
 
    @dbus.service.method('org.social_bar.view')
    def restore(self):
        self.view.show()
    
    def main(self):
        self.view = SocialBarView()
        self.view.main()

if __name__ == "__main__":
    running = False
    try:
        running = DBusSingleAppInstance.is_running()
    except:
        pass
    if running:
        bus = dbus.SessionBus()
        social_bar = bus.get_object('org.social_bar.view', '/org/social_bar/view')
        restore = social_bar.get_dbus_method('restore', 'org.social_bar.view')
        restore()
    else:
        app = SocialBarDbus()
        # FIXME: Get rid of the following line which has the only purpose of
        # working around Ctrl+C not exiting Gtk applications from bug 622084.
        # https://bugzilla.gnome.org/show_bug.cgi?id=622084
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app.main()

