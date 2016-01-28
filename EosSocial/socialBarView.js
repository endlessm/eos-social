// -*- mode: js; js-indent-level: 4; indent-tabs-mode: nil -*-

const Gdk = imports.gi.Gdk;
const GdkX11 = imports.gi.GdkX11;
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;
const Signals = imports.signals;
const Soup = imports.gi.Soup;
const WebKit = imports.gi.WebKit2;

const EosSocialPrivate = imports.gi.EosSocialPrivate;

const ParseUri = imports.parseUri;
const WMInspect = imports.wmInspect;

const SOCIAL_BAR_HOMEPAGE = 'https://m.facebook.com';
const CANCELED_REQUEST_URI = 'about:blank';
const FB_LINK_REDIRECT_KEY = '/render_linkshim_';
const SOCIAL_BAR_WIDTH = 420;
const MAX_FRACTION_OF_DISPLAY_WIDTH = 0.35;
const SIDE_COMPONENT_ROLE = 'eos-side-component';

function _parseLinkFromRedirect(uri) {
    let parser = ParseUri.parseUri(uri);
    let queryDict = parser.queryKey;

    return GLib.uri_unescape_string(queryDict['u'], '');
};

const ANIMATION_TIME = (500 * 1000); // half a second

const BASE_DPI = 96; // base DPI when no font scaling is applied.

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
                      role: SIDE_COMPONENT_ROLE,
                      application: application });
        this.get_style_context().add_class('socialbar-toplevel');

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

        this._fileChooserRequest = null;

        // now create the view
        this._createView();
        this._updateGeometry();

        this._networkMonitor = Gio.NetworkMonitor.get_default();
        this._networkMonitor.connect('notify::network-available', Lang.bind(this,
            this._onNetworkAvailable));
    },

    hide: function() {
        if (this._fileChooser != null) {
            this._fileChooser.response(Gtk.ResponseType.DELETE_EVENT);
            this._fileChooser = null;
        }

        this.parent();
    },

    _onRunFileChooser: function(webView, request) {
        let fileChooser = new Gtk.FileChooserDialog({ action: Gtk.FileChooserAction.OPEN,
                                                      transient_for: this,
                                                      select_multiple: request.select_multiple,
                                                      filter: request.filter });
        fileChooser.add_button(_("Cancel"), Gtk.ResponseType.CANCEL);
        fileChooser.add_button(_("Open"), Gtk.ResponseType.ACCEPT);

        let selectedFiles = request.get_selected_files();
        if (selectedFiles != null) {
            selectedFiles.forEach(function(file) {
                fileChooser.select_filename(file);
            });
        }

        this._fileChooser = fileChooser;
        fileChooser.connect('response', Lang.bind(this, function(dialog, response) {
            if (response == Gtk.ResponseType.ACCEPT) {
                let filenames = this._fileChooser.get_filenames();
                request.select_files(filenames);
            } else {
                request.cancel();
            }

            this._fileChooser.destroy();
            this._fileChooser = null;
        }));

        fileChooser.show_all();

        return true;
    },

    _onActiveWindowChanged: function(wmInspect, activeWindow) {
        // try to match the own window first
        let activeXid = activeWindow.get_xid();
        let xid = this.get_window().get_xid();

        if (xid == activeXid) {
            return;
        }

        // try to match transient windows
        let transientWindow = activeWindow.get_transient();
        let transientXid = 0;

        if (transientWindow != null) {
            transientXid = transientWindow.get_xid();
        }

        if (xid == transientXid) {
            return;
        }

        // no matches - hide our own window
        this.hide();
    },

    _onMonitorsChanged: function() {
        this._updateGeometry();
    },

    _getWorkArea: function() {
        let screen = Gdk.Screen.get_default();
        let monitor = screen.get_primary_monitor();
        let workArea = screen.get_monitor_workarea(monitor);

        return workArea;
    },

    _getSize: function() {
        let workArea = this._getWorkArea();
        let maxWidth = workArea.width * MAX_FRACTION_OF_DISPLAY_WIDTH;
        return [Math.min(SOCIAL_BAR_WIDTH, maxWidth), workArea.height];
    },

    _updateGeometry: function() {
        let workArea = this._getWorkArea();
        let [width, height] = this._getSize();
        let x = workArea.x;

        if (this.get_direction() == Gtk.TextDirection.LTR) {
            x += workArea.width - width;
        }

        let geometry = { x: x,
                         y: workArea.y,
                         width: width,
                         height: height };

        this.move(geometry.x, geometry.y);
        this.resize(geometry.width, geometry.height);
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

        this._browser = new EosSocialPrivate.WebView();
        this._browser.connect('resource-load-started', Lang.bind(this,
            this._resourceHandler));
        this._browser.connect('decide-policy', Lang.bind(this,
            this._policyHandler));
        this._browser.connect('context-menu', Lang.bind(this,
            this._onContextMenu));

        this._browser.connect('load-changed', Lang.bind(this,
            this._updateNavigationFlags));
        this._browser.connect('load-failed-2', Lang.bind(this,
            this._onLoadFailed));
        this._browser.connect('run-file-chooser', Lang.bind(this,
            this._onRunFileChooser));
        this._browser.connect('notify::uri', Lang.bind(this,
            this._updateNavigationFlags));
        this._updateNavigationFlags();

        this._browser.connect('web-process-crashed',
                              Lang.bind(this, function() {
                                  this._browser.reload();
                              }));

        this._browser.setup ();

        let settings = this._browser.get_settings();
        settings.javascript_can_open_windows_automatically = true;

        // Adjust the default font size depending on the text scaling factor.
        let gtk_settings = Gtk.Settings.get_for_screen(this.get_screen());
        this._updateZoomLevelFromGtkSettings(gtk_settings);
        gtk_settings.connect('notify::gtk-xft-dpi', Lang.bind (this, this._updateZoomLevelFromGtkSettings));

        this._initCookies();

        this._browser.vexpand = true;
        let browserFrame = new Gtk.Frame({ shadow_type: Gtk.ShadowType.NONE });
        browserFrame.get_style_context().add_class('socialbar-browser-frame');
        browserFrame.add(this._browser);
        box.add(browserFrame);
        this._browser.load_uri(SOCIAL_BAR_HOMEPAGE);

        frame.show_all();
        this.realize();
    },

    _initCookies: function() {
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

    _updateZoomLevelFromGtkSettings: function (gtk_settings) {
        // The xft-dpi property stores DPI in 1024 * dots/inch.
        let dpi = gtk_settings.gtk_xft_dpi / 1024;

        // We can't use the usual approach used everywhere else (yelp, knowledge apps...)
        // because facebook.com does not use relative units for font-size (it uses 'px'),
        // so changing the default font size won't work, and we use the zoom level instead.
        // That said, the facebook bar seems to work better when scaling everything and not
        // just the text, so we leave the default for WebKitSetting 'zoom-text-only' (FALSE).
        this._browser.set_zoom_level(dpi / BASE_DPI);
    },

    _onNetworkAvailable: function(networkMonitor) {
        let available = networkMonitor.network_available;
        if (!available) {
            return;
        }

        let connectable = null;
        try {
            connectable = Gio.NetworkAddress.parse_uri(SOCIAL_BAR_HOMEPAGE, 80);
        } catch (e) {
            log('Unable to create connectable for social bar URI: ' + e.message);
            return;
        }

        networkMonitor.can_reach_async(connectable, null, Lang.bind(this, function(object, res) {
            try {
                let canReach = networkMonitor.can_reach_finish(res);
                if (canReach) {
                    this._browser.reload();
                }
            } catch (e) {
                log('Unable to verify connection to social bar URI: ' + e.message);
            }
        }));
    },

    _loadOfflinePage: function(uri) {
        let html = null;

        try {
            let htmlBytes = Gio.resources_lookup_data('/com/endlessm/socialbar/offline.html', 0);
            let cssBytes = Gio.resources_lookup_data('/com/endlessm/socialbar/offline.css', 0);
            let imgBytes = Gio.resources_lookup_data('/com/endlessm/socialbar/offline.png', 0);
            let imgBase64 = GLib.base64_encode(imgBytes.toArray());
            let str = _("You’re not online! Connect your<br>internet to access Facebook.");

            html = htmlBytes.get_data().toString().format(cssBytes.toArray(), imgBase64, str);
            this._browser.load_alternate_html(html, uri, uri);
        } catch (e) {
            log('Unable to load HTML offline page from GResource ' + e.message);
        }

        this._updateNavigationFlags();
    },

    _onLoadFailed: function(browser, loadEvent, uri, error) {
        // if we know we're offline, just show the page immediately
        if (!this._networkMonitor.network_available) {
            this._loadOfflinePage(uri);
            return true;
        }

        // now check the error status we got from WebKit
        if (error.domain != Soup.http_error_quark() &&
            !error.matches(WebKit.NetworkError, WebKit.NetworkError.FAILED) &&
            !error.matches(WebKit.NetworkError, WebKit.NetworkError.TRANSPORT) &&
            !error.matches(WebKit.NetworkError, WebKit.NetworkError.UNKNOWN_PROTOCOL) &&
            !error.matches(WebKit.NetworkError, WebKit.NetworkError.FILE_DOES_NOT_EXIST) &&
            !error.matches(WebKit.PolicyError, WebKit.PolicyError.FAILED) &&
            !error.matches(WebKit.PolicyError, WebKit.PolicyError.CANNOT_SHOW_MIME_TYPE) &&
            !error.matches(WebKit.PolicyError, WebKit.PolicyError.CANNOT_SHOW_URI) &&
            !error.matches(WebKit.PolicyError, WebKit.PolicyError.CANNOT_USE_RESTRICTED_PORT) &&
            !error.matches(WebKit.PluginError, WebKit.PluginError.FAILED) &&
            !error.matches(WebKit.PluginError, WebKit.PluginError.CANNOT_FIND_PLUGIN) &&
            !error.matches(WebKit.PluginError, WebKit.PluginError.CANNOT_LOAD_PLUGIN) &&
            !error.matches(WebKit.PluginError, WebKit.PluginError.JAVA_UNAVAILABLE) &&
            !error.matches(WebKit.PluginError, WebKit.PluginError.CONNECTION_CANCELLED))
        {
            // another unhandled error
            return false;
        }

        this._loadOfflinePage(uri);
        return true;
    },

    _onActionMinimize: function() {
        this.hide();
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

    _onContextMenu: function(view, contextMenu, event, hitTestResult) {
        let uri = hitTestResult.get_link_uri();
        if (!uri) {
            return false;
        }

        let position = -1;
        let items = contextMenu.get_items();
        for (let i = 0; i < items.length; i++) {
            if (items[i].get_stock_action() == WebKit.ContextMenuAction.OPEN_LINK_IN_NEW_WINDOW) {
                position = i;
                contextMenu.remove(items[i]);
                break;
            }
        }

        let newItem = WebKit.ContextMenuItem.new_from_stock_action(WebKit.ContextMenuAction.OPEN_LINK_IN_NEW_WINDOW);
        newItem.get_action().connect('activate', Lang.bind(this, function() {
            this._openExternalPage(uri);
        }));

        if (position >= 0) {
            contextMenu.insert(newItem, position);
        } else {
            contextMenu.append(newItem);
        }

        return false;
    },

    _openExternalPage: function(uri) {
        Gtk.show_uri(null, uri, Gtk.get_current_event_time());
    }
});
