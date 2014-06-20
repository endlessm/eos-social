// -*- mode: js; js-indent-level: 4; indent-tabs-mode: nil -*-

const Lang = imports.lang;
const Signals = imports.signals;
const Wnck = imports.gi.Wnck;

const WMInspect = new Lang.Class({
    Name: 'WMInspect',

    _init: function() {
        this._screen = Wnck.Screen.get_default();
        this._screen.connect('active-window-changed', Lang.bind(this,
            this._onActiveWindowChanged));
    },

    _onActiveWindowChanged: function() {
        let activeWindow = this._screen.get_active_window();

        if (!activeWindow)
            return;

        this.emit('active-window-changed', activeWindow);
    }
});
Signals.addSignalMethods(WMInspect.prototype);
