const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;

const SocialBarView = imports.socialBarView;

const SOCIAL_BAR_NAME = 'com.endlessm.SocialBar';
const SOCIAL_BAR_PATH = '/com/endlessm/SocialBar';
const SOCIAL_BAR_IFACE = 'com.endlessm.SocialBar';

const SocialBarIface = <interface name={SOCIAL_BAR_NAME}>
<method name="toggle"/>
<property name="Visible" type="b" access="read"/>
</interface>;

const SocialBar = new Lang.Class({
    Name: 'SocialBar',
    Extends: Gtk.Application,

    _init: function() {
        this.parent({ application_id: SOCIAL_BAR_NAME });
        this.Visible = false;

        this._dbusImpl = Gio.DBusExportedObject.wrapJSObject(SocialBarIface, this);
        this._dbusImpl.export(Gio.DBus.session, SOCIAL_BAR_PATH);
    },

    vfunc_startup: function() {
        this.parent();

        this._window = new SocialBarView.SocialBarView(this);
        this._window.connect('visibility-changed', Lang.bind(this, this._onVisibilityChanged));
    },

    vfunc_activate: function() {
        // do nothing
    },

    toggle: function() {
        this._window.toggle();
    },

    _onVisibilityChanged: function() {
        this.Visible = this._window.getVisible();
        let propChangedVariant = new GLib.Variant('(sa{sv}as)',
            [SOCIAL_BAR_IFACE, { 'Visible': new GLib.Variant('b', this.Visible) }, []]);

        Gio.DBus.session.emit_signal(null, SOCIAL_BAR_PATH,
                                     'org.freedesktop.DBus.Properties',
                                     'PropertiesChanged',
                                     propChangedVariant);
    }
});
