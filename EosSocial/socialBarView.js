const Gdk = imports.gi.Gdk;
const GdkX11 = imports.gi.GdkX11;
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;
const Signals = imports.signals;
const WebKit = imports.gi.WebKit;

const FrameClock = imports.frameClock;
const ParseUri = imports.parseUri;
const WMInspect = imports.wmInspect;

const SOCIAL_BAR_HOMEPAGE = 'https://m.facebook.com';
const CANCELED_REQUEST_URI = 'about:blank';
const FB_LINK_REDIRECT_KEY = '/render_linkshim_';

function _parseLinkFromRedirect(uri) {
    let parser = ParseUri.parseUri(uri);
    let queryDict = parser.queryKey;

    return GLib.uri_unescape_string(queryDict['u'], '');
};

const ANIMATION_TIME = (500 * 1000); // half a second

const SocialBarSlider = new Lang.Class({
    Name: 'SocialBarSlider',
    Extends: FrameClock.FrameClockAnimator,

    _init: function(widget) {
        this._showing = false;
        this.parent(widget, ANIMATION_TIME);
    },

    _getX: function(forVisibility) {
        let [width, height] = this._getSize();
        let workarea = this._getWorkarea();
        let x = workarea.x + workarea.width;

        if (forVisibility) {
            x -= width;
        }

        return x;
    },

    _getInitialValue: function() {
        return this._getX(!this.showing);
    },

    setValue: function(newX) {
        let [, oldY] = this._widget.get_position();
        this._widget.move(newX, oldY);
    },

    _getWorkarea: function() {
        let screen = Gdk.Screen.get_default();
        let monitor = screen.get_primary_monitor();
        let workarea = screen.get_monitor_workarea(monitor);

        return workarea;
    },

    _getSize: function() {
        let workarea = this._getWorkarea();
        return [workarea.width / 3, workarea.height];
    },

    _updateGeometry: function() {
        let workarea = this._getWorkarea();
        let [width, height] = this._getSize();
        let x = this._getX(this.showing);

        let geometry = { x: x,
                         y: workarea.y,
                         width: width,
                         height: height };

        this._widget.move(geometry.x, geometry.y);
        this._widget.set_size_request(geometry.width, geometry.height);
    },

    setInitialValue: function() {
        this.stop();
        this._updateGeometry();
    },

    slideIn: function() {
        if (this.showing) {
            return;
        }

        this.setInitialValue();
        this._widget.show();

        this.showing = true;
        this.start(this._getX(true));
    },

    slideOut: function() {
        if (!this.showing) {
            return;
        }

        this.showing = false;
        this.start(this._getX(false), Lang.bind(this,
            function() {
                this._widget.hide();
            }));
    },

    set showing(value) {
        this._showing = value;
        this.emit('visibility-changed');
    },

    get showing() {
        return this._showing;
    }
});
Signals.addSignalMethods(SocialBarSlider.prototype);

const SocialBarView = new Lang.Class({
    Name: 'SocialBarView',
    Extends: Gtk.ApplicationWindow,
    Signals: {
        'visibility-changed': { }
    },

    _init: function(application) {
        this.parent({ type: Gtk.WindowType.TOPLEVEL,
                      type_hint: Gdk.WindowTypeHint.DOCK,
                      application: application });

        this._wmInspect = new WMInspect.WMInspect();
        this._wmInspect.connect('active-window-changed', Lang.bind(this,
            this._onActiveWindowChanged));

        // stick on all desktop
        this.stick();
        // do not destroy on delete event
        this.connect('delete-event', Lang.bind(this,
            this.hide_on_delete));

        // update position when workarea changes
        let screen = Gdk.Screen.get_default();
        screen.connect('monitors-changed', Lang.bind(this,
            this._onMonitorsChanged));

        // initialize animator
        this._animator = new SocialBarSlider(this);
        this._animator.connect('visibility-changed', Lang.bind(this, this._onVisibilityChanged));

        // now create the view
        this._createView();

        this._animator.setInitialValue();
    },

    _onActiveWindowChanged: function(wmInspect, activeXid) {
        let xid = this.get_window().get_xid();
        if (xid != activeXid) {
            this._animator.slideOut();
        }
    },

    _onMonitorsChanged: function() {
        this._animator.setInitialValue();
    },

    toggle: function() {
        if (this._animator.showing) {
            this._animator.slideOut();
        } else {
            this._animator.slideIn();
            this.present();
        }
    },

    getVisible: function() {
        return this._animator.showing;
    },

    _createView: function() {
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

        container.show_all();
        this.realize();
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
    },

    _onVisibilityChanged: function() {
        // forward the signal
        this.emit('visibility-changed');
    }
});
