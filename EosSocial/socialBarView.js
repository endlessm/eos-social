const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;
const WebKit = imports.gi.WebKit;

const MainWindow = imports.mainWindow;
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
    Extends: MainWindow.MainWindow,

    _init: function(params) {
        this.parent(params);
        this._installActions();

        this._browser = new WebKit.WebView();
        this._browser.connect('resource-request-starting', Lang.bind(this,
            this._resourceHandler));
        this._browser.connect('new-window-policy-decision-requested', Lang.bind(this,
            this._newWindowHandler));

        let settings = this._browser.get_settings();
        settings.javascript_can_open_windows_automatically = true;

        let container = new Gtk.ScrolledWindow();
        container.add(this._browser);

        this.add(container);
        this._browser.load_uri(SOCIAL_BAR_HOMEPAGE);

        this.show_all();
        this.hide();
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

        actions.forEach(Lang.bind(this,
            function(actionEntry) {
                let action = new Gio.SimpleAction({ name: actionEntry.name });
                action.connect('activate', Lang.bind(this, actionEntry.callback));

                this.application.add_accelerator(actionEntry.accel,
                    'win.' + actionEntry.name, null);
                this.add_action(action);
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
