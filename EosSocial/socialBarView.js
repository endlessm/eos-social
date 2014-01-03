const Gdk = imports.gi.Gdk;
const GdkX11 = imports.gi.GdkX11;
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;
const Signals = imports.signals;
const WebKit = imports.gi.WebKit2;

const FrameClock = imports.frameClock;
const ParseUri = imports.parseUri;
const WMInspect = imports.wmInspect;

const SOCIAL_BAR_HOMEPAGE = 'https://m.facebook.com';
const CANCELED_REQUEST_URI = 'about:blank';
const FB_LINK_REDIRECT_KEY = '/render_linkshim_';
const SOCIAL_BAR_WIDTH = 420;
const MAX_FRACTION_OF_DISPLAY_WIDTH = 0.35;
const USER_AGENT_OVERRIDE = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11';

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
        this._willShow = false;
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
        let maxWidth = workarea.width * MAX_FRACTION_OF_DISPLAY_WIDTH;
        return [Math.min(SOCIAL_BAR_WIDTH, maxWidth), workarea.height];
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
        this._widget.resize(geometry.width, geometry.height);
    },

    setInitialValue: function() {
        this.stop();
        this._updateGeometry();
    },

    slideIn: function() {
        if (this._willShow) {
            return;
        }

        this.setInitialValue();
        this._widget.show();

        this._willShow = true;
        this.showing = true;
        this.start(this._getX(false), this._getX(true));
    },

    slideOut: function() {
        if (!this._willShow) {
            return;
        }

        this._willShow = false;
        this.start(this._getX(true), this._getX(false),
                   Lang.bind(this, function() {
                                 this.showing = false;
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

const SocialBarTopbar = new Lang.Class({
    Name: 'SocialBarTopbar',
    Extends: Gtk.Toolbar,

    _init: function(params) {
        this.parent(params);

        this.get_style_context().add_class('socialbar-topbar');

        let leftButtons = new Gtk.Box({ spacing: 6 });
        let leftItem = new Gtk.ToolItem({ child: leftButtons });
        leftItem.set_expand(true);
        this.add(leftItem);

        let backButton = new Gtk.Button({ child: new Gtk.Image({ pixel_size: 16,
                                                                 icon_name: 'topbar-go-previous-symbolic' }),
                                          action_name: 'win.back'
                                        });
        leftButtons.add(backButton);

        let forwardButton = new Gtk.Button({ child: new Gtk.Image({ pixel_size: 16,
                                                                    icon_name: 'topbar-go-next-symbolic' }),
                                             action_name: 'win.forward'
                                           });
        leftButtons.add(forwardButton);
        
        let reloadButton = new Gtk.Button({ child: new Gtk.Image({ pixel_size: 16,
                                                                   icon_name: 'topbar-refresh-symbolic' }),
                                             action_name: 'win.reload'
                                           });
        leftButtons.add(reloadButton);

        let rightButtons = new Gtk.Box({ spacing: 6 });
        this.add(new Gtk.ToolItem({ child: rightButtons }));

        let minimizeButton = new Gtk.Button({ child: new Gtk.Image({ pixel_size: 16,
                                                                     icon_name: 'window-minimize-symbolic' }),
                                              action_name: 'win.minimize'
                                            });
        rightButtons.add(minimizeButton);
    }
});

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

        let visual = screen.get_rgba_visual();
        if (visual) {
            this.set_visual(visual);
        }

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

    toggle: function(timestamp) {
        if (this._animator.showing) {
            this._animator.slideOut();
        } else {
            this._animator.slideIn();
            this.present_with_time(timestamp);
        }
    },

    getVisible: function() {
        return this._animator.showing;
    },

    _createView: function() {
        this._installActions();

        let frame = new Gtk.Frame({ shadow_type: Gtk.ShadowType.IN });
        frame.get_style_context().add_class('socialbar-frame');
        this.add(frame);

        let box = new Gtk.Box({ orientation: Gtk.Orientation.VERTICAL });
        frame.add(box);

        let toolbar = new SocialBarTopbar();
        box.add(toolbar);

        this._browser = new WebKit.WebView();
        this._browser.connect('resource-load-started', Lang.bind(this,
            this._resourceHandler));
        this._browser.connect('decide-policy', Lang.bind(this,
            this._policyHandler));

        this._browser.connect('load-changed', Lang.bind(this,
            this._updateNavigationFlags));
        this._browser.connect('load-failed', Lang.bind(this,
            this._updateNavigationFlags));
        this._browser.connect('notify::uri', Lang.bind(this,
            this._updateNavigationFlags));
        this._updateNavigationFlags();

        let settings = this._browser.get_settings();
        settings.javascript_can_open_windows_automatically = true;
        settings.user_agent = USER_AGENT_OVERRIDE;

        this._initCookies();

        this._browser.vexpand = true;
        box.add(this._browser);
        this._browser.load_uri(SOCIAL_BAR_HOMEPAGE);

        frame.show_all();
        this.realize();
    },

    _initCookies: function() {
        // Use the same as eos-browser
        let webContext = WebKit.WebContext.get_default();
        let cookieManager = webContext.get_cookie_manager();
        let cookiesDir = GLib.build_filenamev([GLib.get_user_config_dir(),
                                               'eos-social']);
        let cookiesFile = GLib.build_filenamev([cookiesDir,
                                               'cookies.sqlite']);

        GLib.mkdir_with_parents(cookiesDir, parseInt(700, 8));
        cookieManager.set_persistent_storage(cookiesFile, WebKit.CookiePersistentStorage.SQLITE);
    },

    _updateNavigationFlags: function() {
        let backAction = this.lookup_action('back');
        backAction.set_enabled(this._browser.can_go_back());

        let forwardAction = this.lookup_action('forward');
        forwardAction.set_enabled(this._browser.can_go_forward());
    },

    _onActionMinimize: function() {
        if (!this.getVisible()) {
            return;
        }

        this.toggle();
    },

    _onActionBack: function() {
        this._browser.go_back();
    },

    _onActionForward: function() {
        this._browser.go_forward();
    },
    
    _onActionReload: function() {
        this._browser.reload();
    },

    _installActions: function() {
        let actions = [{ name: 'back',
                         callback: this._onActionBack,
                         accel: '<Alt>Left' },
                       { name: 'forward',
                         callback: this._onActionForward,
                         accel: '<Alt>Right' },
                       { name: 'reload',
                         callback: this._onActionReload,
                         accel: '<Control>r' },
                       { name: 'minimize',
                         callback: this._onActionMinimize }];

        actions.forEach(Lang.bind(this,
            function(actionEntry) {
                let action = new Gio.SimpleAction({ name: actionEntry.name });
                action.connect('activate', Lang.bind(this, actionEntry.callback));

                if (actionEntry.accel) {
                    this.application.add_accelerator(actionEntry.accel,
                        'win.' + actionEntry.name, null);
                }
                this.add_action(action);
            }));
    },

    _resourceHandler: function(view, resource, request) {
        let uri = request.get_uri();
        if (uri.indexOf(FB_LINK_REDIRECT_KEY) != -1) {
            let link = _parseLinkFromRedirect(uri);
            this._openExternalPage(link);

            request.set_uri(CANCELED_REQUEST_URI);
        }
    },

    _policyHandler: function(view, decision, decisionType) {
        if (decisionType == WebKit.PolicyDecisionType.NEW_WINDOW_ACTION) {
            let request = decision.get_request();
            this._openExternalPage(request.get_uri());
            decision.ignore();

            return true;
        }

        return false;
    },

    _openExternalPage: function(uri) {
        Gtk.show_uri(null, uri, Gtk.get_current_event_time());
    },

    _onVisibilityChanged: function() {
        // forward the signal
        this.emit('visibility-changed');
    }
});
