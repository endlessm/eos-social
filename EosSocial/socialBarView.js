const Gdk = imports.gi.Gdk;
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;
const WebKit = imports.gi.WebKit;

const ParseUri = imports.parseUri;

const SOCIAL_BAR_HOMEPAGE = 'https://m.facebook.com';
const CANCELED_REQUEST_URI = 'about:blank';
const FB_LINK_REDIRECT_KEY = '/render_linkshim_';

function _parseLinkFromRedirect(uri) {
    let parser = ParseUri.parseUri(uri);
    let queryDict = parser.queryKey;

    return GLib.uri_unescape_string(queryDict['u'], '');
};

const SocialBarView = new Lang.Class({
    Name: 'SocialBarView',
    Extends: Gtk.Plug,

    _init: function(socketId) {
        this.parent();
        this.construct(socketId);

        this._installActions();

        // update position when workarea changes
        let screen = Gdk.Screen.get_default();
        screen.connect('monitors-changed', Lang.bind(this,
            this._ensurePosition));

        this._browser = new WebKit.WebView();
        this._browser.connect('resource-request-starting', Lang.bind(this,
            this._resourceHandler));
        this._browser.connect('new-window-policy-decision-requested', Lang.bind(this,
            this._newWindowHandler));

        let settings = this._browser.get_settings();
        settings.javascript_can_open_windows_automatically = true;

        let container = new Gtk.ScrolledWindow();
        container.add(this._browser);
        container.show_all();

        this.add(container);
        this._browser.load_uri(SOCIAL_BAR_HOMEPAGE);

        this.realize();
    },

    _ensurePosition: function() {
        let screen = Gdk.Screen.get_default();
        let monitor = screen.get_primary_monitor();
        let workarea = screen.get_monitor_workarea(monitor);

        let width = workarea.width / 3;
        let geometry = { x: workarea.x + workarea.width - width,
                         y: workarea.y,
                         width: width,
                         height: workarea.height };

        this.move(geometry.x, geometry.y);
        this.set_size_request(geometry.width, geometry.height);
    },

    toggle: function() {
        if (this.get_visible()) {
            this.hide();
        } else {
            this._ensurePosition()
            this.show();
        }
    },

    _onActionBack: function() {
        this._browser.go_back();
    },

    _onActionForward: function() {
        this._browser.go_forward();
    },

    _installActions: function() {
        let actions = [{ name: 'back',
                         callback: this._onActionBack,
                         accel: '<Alt>Left' },
                       { name: 'forward',
                         callback: this._onActionForward,
                         accel: '<Alt>Right' }];

        let application = Gio.Application.get_default();

        actions.forEach(Lang.bind(this,
            function(actionEntry) {
                let action = new Gio.SimpleAction({ name: actionEntry.name });
                action.connect('activate', Lang.bind(this, actionEntry.callback));

                application.add_accelerator(actionEntry.accel,
                    'app.' + actionEntry.name, null);
                application.add_action(action);
            }));
    },

    _resourceHandler: function(view, frame, resource, request, response) {
        let uri = request.get_uri();
        if (uri.indexOf(FB_LINK_REDIRECT_KEY) != -1) {
            let link = _parseLinkFromRedirect(uri);
            this._openExternalPage(link);

            request.set_uri(CANCELED_REQUEST_URI);
        }
    },

    _newWindowHandler: function(view, frame, request, action, decision) {
        this._openExternalPage(request.get_uri());
        decision.ignore();

        return true;
    },

    _openExternalPage: function(uri) {
        Gtk.show_uri(null, uri, Gtk.get_current_event_time());
    }
});
