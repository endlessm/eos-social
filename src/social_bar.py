#!/usr/bin/env python
from social_bar_view import SocialBarView
from social_bar_presenter import SocialBarPresenter
from social_bar_model import SocialBarModel
from util.single_instance import DBusSingleAppInstance
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import subprocess
 
class SocialBarDbus(dbus.service.Object):
    DBusGMainLoop(set_as_default=True)
    def __init__(self):
        bus_name = dbus.service.BusName('org.social_bar.view', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/social_bar/view')
 
    @dbus.service.method('org.social_bar.view')
    def restore(self):
        self.presenter.get_view().deiconify()
    
    def main(self):
        #try:
            #subprocess.Popen(['python', '/usr/share/eos-social/util/webserver.pyc'], stdout=subprocess.PIPE)
        #except:
        #    pass
        self.presenter = SocialBarPresenter(SocialBarView(), SocialBarModel())
        self.presenter.get_view().set_presenter(self.presenter)
        self.presenter.get_view().main()

if __name__ == "__main__":
    running = False
    try:
        running = DBusSingleAppInstance.is_running()
    except:
        pass
    if running:
        #print "Social Bar already running!"
        bus = dbus.SessionBus()
        social_bar = bus.get_object('org.social_bar.view', '/org/social_bar/view')
        restore = social_bar.get_dbus_method('restore', 'org.social_bar.view')
        restore()
    else:
        app = SocialBarDbus()
        app.main()

