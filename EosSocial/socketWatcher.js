const Gio = imports.gi.Gio;
const Lang = imports.lang;
const Signals = imports.signals;

const SOCKET_EXPORTER_NAME = 'com.endlessm.SocketExporter';
const SOCKET_EXPORTER_PATH = '/com/endlessm/SocketExporter';
const SOCKET_EXPORTER_IFACE = 'com.endlessm.SocketExporter';

const SocketExporterIface = <interface name={SOCKET_EXPORTER_IFACE}>
    <method name="GetSocketId">
    <arg type="u" direction="out"/>
    </method>
    </interface>;
var SocketExporterProxy = Gio.DBusProxy.makeProxyWrapper(SocketExporterIface);

const SocketWatcher = new Lang.Class({
    Name: 'SocketWatcher',

    _init: function() {
        Gio.DBus.session.watch_name(SOCKET_EXPORTER_NAME, Gio.BusNameWatcherFlags.NONE,
                                    Lang.bind(this, this._onSocketAppeared),
                                    Lang.bind(this, this._onSocketVanished));
    },

    _onSocketAppeared: function() {
        this._proxy = new SocketExporterProxy(Gio.DBus.session,
            SOCKET_EXPORTER_NAME,
            SOCKET_EXPORTER_PATH,
            Lang.bind(this, this._onProxyConstructed));
    },

    _onProxyConstructed: function() {
        this._proxy.GetSocketIdRemote(Lang.bind(this, this._onGetSocketId));
    },

    _onGetSocketId: function(result, error) {
        if (error) {
            this._onSocketVanished();
            return;
        }

        let id = result[0];
        this.emit('socket-available', id);
    },

    _onSocketVanished: function() {
        this._proxy = null;
        this.emit('socket-destroyed');
    }
});
Signals.addSignalMethods(SocketWatcher.prototype);
