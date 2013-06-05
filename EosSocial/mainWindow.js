const Gdk = imports.gi.Gdk;
const GdkX11 = imports.gi.GdkX11;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;

const WMInspect = imports.wmInspect;

const MainWindow = new Lang.Class({
    Name: 'MainWindow',
    Extends: Gtk.ApplicationWindow,

    _init: function(application) {
        this.parent({ type: Gtk.WindowType.TOPLEVEL,
                      application: application,
                      decorated: false,
                      modal: true,
                      resizable: false,
                      skip_pager_hint: true,
                      skip_taskbar_hint: true });

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
            this._ensurePosition));
    },

    _onActiveWindowChanged: function(wmInspect, activeXid) {
        let xid = this.get_window().get_xid();
        if (xid != activeXid)
            this.hide();
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

    show: function() {
        this._ensurePosition();
        this.present();
    },

    toggle: function() {
        if (this.get_visible())
            this.hide();
        else
            this.show();
    }
});
