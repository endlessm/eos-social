const Lang = imports.lang;
const Signals = imports.signals;

// Robert Penner's easeOutQuint
function _easeTime(time) {
    let p = time - 1;
    return -1 * (p * p * p * p - 1);
}

const FrameClockAnimator = new Lang.Class({
    Name: 'FrameClockAnimator',
    Abstract: true,

    _init: function(widget, duration) {
        this._widget = widget;
        this._duration = duration;

        this._tickId = 0;
        this._startTime = 0;
        this._startValue = null;
        this._endValue = null;
        this._endCallback = null;
    },

    start: function(endValue, endCallback) {
        if (this._tickId) {
            this.stop();
        }

        this._tickId = this._widget.add_tick_callback(
            Lang.bind(this, this._onFrameTick));
        this._startTime = this._widget.get_frame_clock().get_frame_time();
        this._startValue = this._getInitialValue();
        this._endValue = endValue;

        if (endCallback) {
            this._endCallback = endCallback;
        } else {
            this._endCallback = null;
        }
    },

    stop: function() {
        if (this._tickId == 0) {
            return;
        }

        this._widget.remove_tick_callback(this._tickId);
        this._tickId = 0;
    },

    _onFrameTick: function(widget, frameClock) {
        let time = (frameClock.get_frame_time() - this._startTime) / this._duration;

        if (time > 1.0) {
            this._tickId = 0;

            if (this._endCallback) {
                this._endCallback();
                this._endCallback = null;
            }

            return false;
        }

        time = _easeTime(time);
        let newValue = this._startValue + (this._endValue - this._startValue) * time;

        this.setValue(newValue);
        return true;
    }
});
Signals.addSignalMethods(FrameClockAnimator.prototype);
