const Gio = imports.gi.Gio;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;
const WebKit = imports.gi.WebKit;

const MainWindow = imports.mainWindow;

const SocialBarView = new Lang.Class({
    Name: 'SocialBarView',
    Extends: MainWindow.MainWindow,

    _init: function(params) {
        this.parent(params);
        this._installActions();

        this._browser = new WebKit.WebView();

        let container = new Gtk.ScrolledWindow();
        container.add(this._browser);

        this.add(container);
        this._browser.load_uri('http://m.facebook.com');

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
    }
});
