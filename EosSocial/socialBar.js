const Gio = imports.gi.Gio;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;

const SocialBarView = imports.socialBarView;

const SOCIAL_BAR_NAME = 'com.endlessm.SocialBar';
const SOCIAL_BAR_PATH = '/com/endlessm/SocialBar';
const SOCIAL_BAR_IFACE = 'com.endlessm.SocialBar';

const SocialBarIface = <interface name={SOCIAL_BAR_NAME}>
<method name="toggle"/>
</interface>;

const SocialBar = new Lang.Class({
    Name: 'SocialBar',
    Extends: Gtk.Application,

    _init: function() {
        this.parent({ application_id: SOCIAL_BAR_NAME });

        this._dbusImpl = Gio.DBusExportedObject.wrapJSObject(SocialBarIface, this);
        this._dbusImpl.export(Gio.DBus.session, SOCIAL_BAR_PATH);
    },

    vfunc_startup: function() {
        this.parent();

        this._window = new SocialBarView.SocialBarView(this);
    },

    vfunc_activate: function() {
        // do nothing
    },

    toggle: function() {
        this._window.toggle();
    }
});
