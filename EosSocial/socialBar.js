const Gdk = imports.gi.Gdk;
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const Gtk = imports.gi.Gtk;
const Lang = imports.lang;

const Path = imports.path;
const SocialBarView = imports.socialBarView;

const SOCIAL_BAR_NAME = 'com.endlessm.SocialBar';
const SOCIAL_BAR_PATH = '/com/endlessm/SocialBar';
const SOCIAL_BAR_IFACE = 'com.endlessm.SocialBar';

const SocialBarIface = <interface name={SOCIAL_BAR_NAME}>
<method name="toggle">
<arg type="u" direction="in" name="timestamp"/>
</method>
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

        let resource = Gio.Resource.load(Path.RESOURCE_DIR + '/eos-social.gresource');
        resource._register();

        let provider = new Gtk.CssProvider();
        provider.load_from_file(Gio.File.new_for_uri('resource:///com/endlessm/socialbar/eos-social.css'));
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION);

        this._window = new SocialBarView.SocialBarView(this);
        this._window.connect('notify::visible', Lang.bind(this, this._onVisibilityChanged));
    },

    vfunc_activate: function() {
        // do nothing
    },

    toggle: function(timestamp) {
        this._window.toggle(timestamp);
    },

    _onVisibilityChanged: function() {
        this.Visible = this._window.is_visible();
        let propChangedVariant = new GLib.Variant('(sa{sv}as)',
            [SOCIAL_BAR_IFACE, { 'Visible': new GLib.Variant('b', this.Visible) }, []]);

        Gio.DBus.session.emit_signal(null, SOCIAL_BAR_PATH,
                                     'org.freedesktop.DBus.Properties',
                                     'PropertiesChanged',
                                     propChangedVariant);
    }
});
