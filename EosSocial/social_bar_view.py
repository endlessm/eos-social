from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import WebKit

from urlparse import urlparse
from urlparse import parse_qs

from main_window import MainWindow


class SocialBarView(MainWindow):
    HOMEPAGE = "https://m.facebook.com/"

    CANCELED_REQUEST_URI = "about:blank"
    FB_LINK_REDIRECT_KEY = "/render_linkshim_"

    ALT = '<Alt>'

    def __init__(self):
        super(SocialBarView, self).__init__()
        self.connect('destroy', self._destroy)
        self._create()

    def create_shortcuts(self, accelgroup=Gtk.AccelGroup()):
        for hotkey, modifier, callback in self._shortcuts:
            key, modifier = Gtk.accelerator_parse(modifier + hotkey)
            accelgroup.connect(key, modifier, Gtk.AccelFlags.VISIBLE, callback)
        self.add_accel_group(accelgroup)

    def _create(self):
        self._browser = WebKit.WebView()
        self._browser.get_settings().set_property('javascript-can-open-windows-automatically', True)

        self._browser.connect("resource-request-starting", self._resource_handler)
        self._browser.connect("new-window-policy-decision-requested", self._new_window_handler)

        self._shortcuts = [('Left', self.ALT, lambda a, widget, c, m: self._browser.go_back()),
                           ('Right', self.ALT, lambda a, widget, c, m: self._browser.go_forward())]
        self.create_shortcuts()

        self.main_container = Gtk.ScrolledWindow()
        self.main_container.add(self._browser)

        self.add(self.main_container)
        self.show_all()
        self.hide()

        self._browser.load_uri(self.HOMEPAGE)

    def _new_window_handler(self, view, frame, request, navigation_action, policy_decision, data=None):
        self._load_in_external_browser(request.get_uri())
        policy_decision.ignore()

        return True

    def _destroy(self, *args):
        Gtk.main_quit()

    def _resource_handler(self, view, frame, resource, request, response, data=None):
        # Facebook uses redirects that don't trigger
        # new-window-policy-decision-requested so we have to watch for this
        # redirect attempt here to intercept it and load it ourselves
        if self.FB_LINK_REDIRECT_KEY in request.get_uri():
            link = self._get_link_from_fb_redirect(request)
            self._load_in_external_browser(link)

            request.set_uri(self.CANCELED_REQUEST_URI)

    def _get_link_from_fb_redirect(self, request):
        uri = request.get_uri()
        query_params = parse_qs(urlparse(uri).query)
        link = query_params['u'][0]

        return link

    def _load_in_external_browser(self, uri):
        Gtk.show_uri(Gdk.Screen.get_default(), uri, Gtk.get_current_event_time())

    def main(self):
        GObject.threads_init()
        Gtk.main()
