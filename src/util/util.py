# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import httplib

def get_data(url):
    try:
        data = urllib2.urlopen(url).read()
        print 'DATA RETRIEVED:\n', data, '\n', '-'*80       
        return json.loads(data)
    except:
        return None

def fb_auth_url(app_id, redirect_url, permissions=None):
    parameters = {'client_id':app_id, 'redirect_uri':redirect_url}
    if permissions:
        parameters['scope'] = ','.join(permissions)
    encoded_parameters = urllib.urlencode(parameters)
    auth_url = 'http://graph.facebook.com/oauth/authorize?'
    auth_url += encoded_parameters
    return auth_url

def delete_like(token, post_id):
    conn = httplib.HTTPSConnection('graph.facebook.com')
    conn.request('DELETE', '/' + post_id + '/likes?access_token=' + token, '') 
    resp = conn.getresponse()
    content = resp.read()
    print content

CSS = ''' @charset "utf-8";
      /* CSS Document */

      body {
        /* background-image:url(../images/bg.png) !important;
        background-repeat:repeat; */
        background: #527CAE;
        }

      .user {
        background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAkAAAAQCAYAAADESFVDAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAVJJREFUeNpiZEAFTFDMDsQ8QMyvo6MjwwSVZARiZijmAGIuqCKezMxMGxYk3axQzAlVwGdubi7l6OgYCFLEApVkhyrgBikSFBQU6OnpyWRnZ+digVrBDrWCF6RAQECAf8WKFWmSkpIqjIyMYGtACtmgbuFwcXGR3bBhQ4mioqI+ExPEySxQh//X1tbmKCgo8DcwMAjk5OTkQPYyS2trqxwQJAoJCTlxcXFx//v3j+Hv379gDDcJyPj8+/fvNz9//vzKzMzMDcRgSRgGuYkRFgTGxsbsOTk5wUDHZvHw8AgCrWTg4OBgAGkC+ew/CD9//vzPxo0br4qLi28FKlRmY2OTg5uGLVpUVFQ4J0yY0ADU4AMyDRsAh76srKzA3r17F164cOEmMxZFIOsZPn36xPD58+dzVlZWnswMuAHTjRs3/llaWn7Hpwgkx/bq1atPAAEGAAAUUHUGoEQ3AAAAAElFTkSuQmCC') no-repeat scroll 38px 10px transparent;
        width: 47px !important;
      }

      .user img {
        -webkit-border-radius: 5px;
        -moz-border-radius: 5px;
        border-radius: 5px;
        -moz-box-shadow: 1px 1px 6px 1px rgba(0, 0, 0, 0.3);
        -webkit-box-shadow: 1px 1px 6px 1px rgba(0, 0, 0, 0.3);
        box-shadow: 1px 1px 6px 1px rgba(0, 0, 0, 0.3);
        height: 32px;
        width: 32px;
      }
            
            .user a {
             color: #121719;
            }

      .post-content {
        background: url('data:image/png;base64,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') no-repeat #D5D5D5 !important;
        background-position: bottom !important;
        color: #000;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 12px;
        float: left;
        padding: 10px 0 6px 12px !important;
        opacity: 0.85;
        -webkit-box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.45);
        -moz-box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.45);
        box-shadow: inset -3px -3px 6px rgba(0,0,0,0.20);
        border-radius: 5px;
        margin-bottom: 25px;
        -webkit-border-radius: 5px;
        -moz-border-radius: 5px;
        width: 296px !important;
      }

      .post-content span {
        color: #000 !important;
        font-size: 12px;
        padding-bottom: 20px;
        margin-bottom: 10px !important;
        text-shadow: 0 1px 0px rgba(255,255,255, 0.5);
      }

      .post-content a {
        color: #2e5790;
        font-size: 12px;
        font-weight:bold;    
        padding-left: 5px;
        text-decoration: none;
        margin-left: -4px !important;
      }

      .link {
        font-size: 12px;
      }

      .imagecls img {
        border: solid 3px #fff;
        margin: 10px 10px 0 -2px;
        max-width: 281px;    
      }

      #comments-count-100001018405810_412445778824455,
      #likes-count-100001018405810_412445778824455 {
        font-size: 11px;
      }

      .like {
        height: 18px;
        width: 42px;
        float: left;
        padding: 3px 6px;
      }

      .like:hover {
        background: #f0f0f0;
      }

      .like img {
        padding-top: 2px;
      }

      .comment {
        height: 18px;
        width: 42px;
        float: right;
        padding: 3px 6px;
      }

      .comment:hover {
        background: #f0f0f0;
      }

      .comment img {
        padding-top: 2px;
      }

      .wrapper {
        display: inline-block;
        height: 17px;
      }
'''
    
SLICKSCROLL_CSS = '''
﻿.slickscrollcontainer
{
    padding: 0px;
    margin: 0px;
    background-color: #CCCCCC;
}

.slickscroll_vertical_scrollbar
{
    position: absolute;
    width: 14px;
    height: 87px;
    background-image: url('data:image/png;base64,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');
    background-repeat: no-repeat;
    cursor:move;
}

.slickscroll_vertical_scrollbar div
{
    background-position: bottom;
    background-image: url('data:image/png;base64,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');
    background-repeat: no-repeat;
    width: 14px;
    height: 15px;
    bottom: 0px;
    position:absolute;
}

.slickscroll_horizontal_scrollbar
{
    position: absolute;
    width: 87px;
    height: 12px;
    background-image: url('../Images/scrollbar_horizontal_leftpart.png');
    background-repeat: no-repeat;
    cursor:move;
}

.slickscroll_horizontal_scrollbar div
{
    background-image: url('../Images/scrollbar_horizontal_rightpart.png');
    background-repeat: no-repeat;
    background-position: right;
    width: 5px;
    height: 12px;
    float:right;
}
'''

MOUSE_WHEEL_JS = '''
/*! Copyright (c) 2011 Brandon Aaron (http://brandonaaron.net)
 * Licensed under the MIT License (LICENSE.txt).
 *
 * Thanks to: http://adomas.org/javascript-mouse-wheel/ for some pointers.
 * Thanks to: Mathias Bank(http://www.mathias-bank.de) for a scope bug fix.
 * Thanks to: Seamus Leahy for adding deltaX and deltaY
 *
 * Version: 3.0.6
 * 
 * Requires: 1.2.2+
 */

(function($) {

var types = ['DOMMouseScroll', 'mousewheel'];

if ($.event.fixHooks) {
    for ( var i=types.length; i; ) {
        $.event.fixHooks[ types[--i] ] = $.event.mouseHooks;
    }
}

$.event.special.mousewheel = {
    setup: function() {
        if ( this.addEventListener ) {
            for ( var i=types.length; i; ) {
                this.addEventListener( types[--i], handler, false );
            }
        } else {
            this.onmousewheel = handler;
        }
    },
    
    teardown: function() {
        if ( this.removeEventListener ) {
            for ( var i=types.length; i; ) {
                this.removeEventListener( types[--i], handler, false );
            }
        } else {
            this.onmousewheel = null;
        }
    }
};

$.fn.extend({
    mousewheel: function(fn) {
        return fn ? this.bind("mousewheel", fn) : this.trigger("mousewheel");
    },
    
    unmousewheel: function(fn) {
        return this.unbind("mousewheel", fn);
    }
});


function handler(event) {
    var orgEvent = event || window.event, args = [].slice.call( arguments, 1 ), delta = 0, returnValue = true, deltaX = 0, deltaY = 0;
    event = $.event.fix(orgEvent);
    event.type = "mousewheel";
    
    // Old school scrollwheel delta
    if ( orgEvent.wheelDelta ) { delta = orgEvent.wheelDelta/120; }
    if ( orgEvent.detail     ) { delta = -orgEvent.detail/3; }
    
    // New school multidimensional scroll (touchpads) deltas
    deltaY = delta;
    
    // Gecko
    if ( orgEvent.axis !== undefined && orgEvent.axis === orgEvent.HORIZONTAL_AXIS ) {
        deltaY = 0;
        deltaX = -1*delta;
    }
    
    // Webkit
    if ( orgEvent.wheelDeltaY !== undefined ) { deltaY = orgEvent.wheelDeltaY/120; }
    if ( orgEvent.wheelDeltaX !== undefined ) { deltaX = -1*orgEvent.wheelDeltaX/120; }
    
    // Add event and delta to the front of the arguments
    args.unshift(event, delta, deltaX, deltaY);
    
    return ($.event.dispatch || $.event.handle).apply(this, args);
}

})(jQuery);
'''

SLICKSCROLL_JS = '''
﻿/*
* jQuery Custom Scrollbar Script Oct 20th
* Visit http://www.dynamicdrive.com/ for full source code
*/

/// <reference path="jquery-1.6.2.js" />

(function ($) {

    $.fn.slickscroll = function (options) {

        var scrollcontainer;
        var scrollcontent;
        var scrollbar
        var scrollcontentpos = new Array(0, 0);
        var scrollcontainerpos = new Array(0, 0);
        var mousewheelscrolltop;
        var ap = false;
        var scrollhw = 0;

        //public methods

        this.InValidate = function () {
            scrollhw = (options.verticalscrollbar ? scrollcontent.prop('scrollHeight') : scrollcontent.prop('scrollWidth'));
            $(window).resize();
        }

        this.scrollBy = function (n, speed) {
            if (options.verticalscrollbar) {
                var scrolltop = scrollcontent.scrollTop() + n;
                if (scrolltop < 0) return;
                scrollcontent.animate({ scrollTop: scrolltop + 'px' }, speed);
                scrollbar.css({ "top": scrollcontainerpos.top + scrolltop / (scrollcontent.prop('scrollHeight') / scrollcontent.height()) + "px" });
            }
            else {
                var scrollleft = scrollcontent.scrollLeft() + n;
                if (scrollleft < 0) return;
                scrollcontent.animate({ scrollLeft: scrollleft + 'px' }, speed);
                scrollbar.css({ "left": scrollcontainerpos.left + scrollleft / (scrollcontent.prop('scrollWidth') / scrollcontent.width()) + "px" });
            }
        };

        this.scrollTop = function (speed) {
            if (options.verticalscrollbar) {
                scrollcontent.animate({ scrollTop: '0px' }, speed);
                scrollbar.animate({ top: scrollcontainerpos.top + 'px' }, speed);
            }
            else {
                scrollcontent.animate({ scrollLeft: '0px' }, speed);
                scrollbar.animate({ left: scrollcontainerpos.left + 'px' }, speed);
            }
        };

        this.scrollBottom = function (speed) {
            if (options.verticalscrollbar) {
                scrollcontent.animate({ scrollTop: scrollcontent.prop('scrollHeight') + 'px' }, speed);
                scrollbar.animate({ top: scrollcontainer.height() - scrollbar.height() + scrollcontainerpos.top + 'px' }, speed);
            }
            else {
                scrollcontent.animate({ scrollLeft: scrollcontent.prop('scrollWidth') + 'px' }, speed);
                scrollbar.animate({ left: scrollcontainer.width() - scrollbar.width() + scrollcontainerpos.left + 'px' }, speed);
            }
        };

        this.scrollTo = function (element, speed) {
            var elpos = element.offset();
            if (elpos == null) return;
            if (options.verticalscrollbar) {
                var scrolltop = elpos.top - (scrollcontent.height() / 2) + scrollcontent.scrollTop() - scrollcontainerpos.top - (ap ? scrollcontainer.offset().top : 0);
                scrollcontent.animate({ scrollTop: scrolltop + 'px' }, speed);
                scrollbar.animate({ top: scrollcontainerpos.top + scrolltop / (scrollcontent.prop('scrollHeight') / scrollcontent.height()) + "px" }, speed);
                if (scrollbar.offset().top + scrollbar.height() > scrollcontent.height()) scrollbar.css({ "top": scrollcontainer.height() - scrollbar.height() + scrollcontainerpos.top + "px" });
            }
            else {
                var scrollleft = elpos.left - (scrollcontent.width() / 2) + scrollcontent.scrollLeft() - scrollcontainerpos.left - (ap ? scrollcontainer.offset().left : 0);
                var scrollbarleft = scrollcontainerpos.left + scrollleft / (scrollcontent.prop('scrollWidth') / scrollcontent.width());
                if (scrollbarleft + scrollbar.width() > scrollcontent.width()) scrollbarleft = scrollcontainer.width() - scrollbar.width() + scrollcontainerpos.left;
                scrollcontent.animate({ scrollLeft: scrollleft + 'px' }, speed);
                scrollbar.animate({ left: scrollbarleft + "px" }, speed);
            }
        };

        //end public methods

        //init

        var defaults = {
            verticalscrollbar: false,
            horizontalscrollbar: false,
            container_class_name: 'slickscrollcontainer',
            vertical_scrollbar_class_name: 'slickscroll_vertical_scrollbar',
            horizontal_scrollbar_class_name: 'slickscroll_horizontal_scrollbar',
            min_scrollbar_size: 25,
            mousewheel_scroll_speed: 5
        }

        if (options != null) {
            if (options.verticalscrollbar == null) options.verticalscrollbar = defaults.verticalscrollbar;
            if (options.horizontalscrollbar == null) options.horizontalscrollbar = defaults.horizontalscrollbar;
            if (options.container_class_name == null) options.container_class_name = defaults.container_class_name;
            if (options.vertical_scrollbar_class_name == null) options.vertical_scrollbar_class_name = defaults.vertical_scrollbar_class_name;
            if (options.horizontal_scrollbar_class_name == null) options.horizontal_scrollbar_class_name = defaults.horizontal_scrollbar_class_name;
            if (options.min_scrollbar_size == null) options.min_scrollbar_size = defaults.min_scrollbar_size;
            if (options.mousewheel_scroll_speed == null) options.mousewheel_scroll_speed = defaults.mousewheel_scroll_speed;
        }
        else {
            options = defaults;
        }

        $(document).unbind("mouseup");

        //end init

        //slickscroll logic
        return this.each(function () {
            scrollcontent = $(this);

            var scrollcontentparent = scrollcontent.parent();

            scrollhw = (options.verticalscrollbar ? scrollcontent.prop('scrollHeight') : scrollcontent.prop('scrollWidth'));

            scrollcontent.wrap('<div class="' + options.container_class_name + '"></div>'); //append the container
            scrollcontainer = scrollcontent.closest('.' + options.container_class_name); //get a ref to the container

            if (scrollcontent.css("position") == "absolute" || scrollcontent.css("position") == "relative") {
                ap = true;
                scrollcontainer.css({ "position": "absolute", "left": scrollcontent.offset().left + "px", "top": scrollcontent.offset().top + "px" });
                scrollcontent.css({ "position": "static" });
            }
            else if (scrollcontentparent.css("position") == "relative" || scrollcontentparent.css("position") == "absolute") {
                ap = true;
                //scrollcontainer.css({ "position": "absolute", "left": scrollcontentparent.offset().left + "px", "top": scrollcontentparent.offset().top + "px" });
                //scrollcontentparent.css({ "position": "static" });
            }

            if (options.verticalscrollbar) {
                scrollcontainer.prepend('<div class="' + options.vertical_scrollbar_class_name + '"><div></div></div>');
                scrollbar = scrollcontainer.children('.' + options.vertical_scrollbar_class_name);
            }
            else {
                scrollcontainer.prepend('<div class="' + options.horizontal_scrollbar_class_name + '"><div></div></div>');
                scrollbar = scrollcontainer.children('.' + options.horizontal_scrollbar_class_name);
            }

            scrollcontainer.mousedown(function (e) {
                if (options.verticalscrollbar) {
                    if (e.pageX < scrollbar.offset().left) return;
                    if (ap)
                        DoScroll(e, e.pageY - (scrollbar.height() / 2), null);
                    else
                        DoScroll(e, e.pageY - scrollcontentpos.top - (scrollbar.height() / 2), null);
                }
                else {
                    if (e.pageY < scrollbar.offset().top) return;
                    if (ap)
                        DoScroll(e, null, e.pageX - (scrollbar.width() / 2));
                    else
                        DoScroll(e, null, e.pageX - scrollcontentpos.left - (scrollbar.width() / 2));
                }
            });

            mousewheelscrolltop = scrollcontent.scrollTop();

            RecalcSize();
            SetIfScrollBarNeedsToBeVisible();

            scrollbar.unbind("mousedown");

            scrollcontent.mousewheel(function (e, delta) {
                if (options.verticalscrollbar) {
                    mousewheelscrolltop = scrollbar.offset().top - scrollcontentpos.top;
                    if (mousewheelscrolltop < 0) mousewheelscrolltop = 5;
                    if (mousewheelscrolltop + scrollbar.height() > scrollcontent.height()) mousewheelscrolltop = scrollcontent.height() - scrollbar.height() - options.mousewheel_scroll_speed;
                    mousewheelscrolltop += (delta < 0 ? options.mousewheel_scroll_speed : (options.mousewheel_scroll_speed * -1));
                    DoScroll(e, mousewheelscrolltop, null, true);
                }
                else {
                    mousewheelscrolltop = scrollbar.offset().left - scrollcontentpos.left;
                    if (mousewheelscrolltop < 0) mousewheelscrolltop = 5;
                    if (mousewheelscrolltop + scrollbar.width() > scrollcontent.width()) mousewheelscrolltop = scrollcontent.width() - scrollbar.width() - options.mousewheel_scroll_speed;
                    mousewheelscrolltop += (delta < 0 ? options.mousewheel_scroll_speed : (options.mousewheel_scroll_speed * -1));
                    DoScroll(e, null, mousewheelscrolltop, true);
                }
        return false
            });

            $(document).mouseup(function () {
                scrollbarmouseoffset = 0;
                $(document).unbind("mousemove");
                enableSelection(scrollcontent.get(0));
                enableSelection(document.body);
            });

            $(document).mouseleave(function () {
                $(document).unbind("mousemove");
                enableSelection(scrollcontent.get(0));
                enableSelection(document.body);
            });

            $(document).mousedown(function () {
                enableSelection(scrollcontent.get(0));
                enableSelection(document.body);
            });

            var scrollbarmouseoffset = 0;

            scrollbar.mousedown(function (e) {
                e.stopPropagation()
                $(document).unbind("mousemove");
                if (options.verticalscrollbar)
                    scrollbarmouseoffset = (e.pageY - scrollbar.offset().top);
                else
                    scrollbarmouseoffset = (e.pageX - scrollbar.offset().left);
                $(document).mousemove(function (e) {
                    DoScroll(e, null, null);
                });
            });

            function DoScroll(e, y, x, mw) {
                var scrollbarpos = scrollbar.offset();

                disableSelection(scrollcontent.get(0));
                disableSelection(document.body);

                if (options.verticalscrollbar) {
                    if (y == null) y = e.pageY - scrollcontainerpos.top - scrollbarmouseoffset;
                    if (ap && !mw) y -= scrollcontentpos.top
                    if (y >= 0) {
                        if (y + scrollbar.height() <= scrollcontainer.height()) {
                            scrollbar.css({ "top": y + scrollcontainerpos.top + "px" });
                            scrollcontent.scrollTop(y * (scrollcontent.prop('scrollHeight') / scrollcontent.height()));
                        }
                        else {
                            scrollbar.css({ "top": scrollcontainer.height() - scrollbar.height() + scrollcontainerpos.top + "px" });
                            scrollcontent.scrollTop(scrollcontent.prop('scrollHeight'));
                        }
                    }
                    else {
                        scrollbar.css({ "top": scrollcontainerpos.top + "px" });
                        scrollcontent.scrollTop(0);
                    }
                }
                else {
                    if (x == null) x = e.pageX - scrollcontainerpos.left - scrollbarmouseoffset;
                    if (ap && !mw) x -= scrollcontentpos.left
                    if (x >= 0) {
                        if (x + scrollbar.width() <= scrollcontainer.width()) {
                            scrollbar.css({ "left": x + scrollcontainerpos.left + "px" });
                            scrollcontent.scrollLeft(x * (scrollcontent.prop('scrollWidth') / scrollcontent.width()));
                        }
                        else {
                            scrollbar.css({ "left": scrollcontainer.width() - scrollbar.width() + scrollcontainerpos.left + "px" });
                            scrollcontent.scrollLeft(scrollcontent.prop('scrollWidth'));
                        }
                    }
                    else {
                        scrollbar.css({ "left": scrollcontainerpos.left + "px" });
                        scrollcontent.scrollLeft(0);
                    }
                }
            }

            $(window).resize(function () {
                RecalcSize();
                SetIfScrollBarNeedsToBeVisible();
            });

            function SetIfScrollBarNeedsToBeVisible() {
                if (options.verticalscrollbar) {
                    if (scrollhw <= scrollcontainer.height()) {
                        scrollbar.hide();
                        scrollcontainer.width(0);
                    }
                    else {
                        scrollbar.show();
                        scrollcontainer.width(null);
                    }
                }
                else {
                    if (scrollhw <= scrollcontainer.width()) {
                        scrollbar.hide();
                        scrollcontainer.height(0);
                    }
                    else {
                        scrollbar.show();
                        scrollcontainer.height(null);
                    }
                }
            }

            function RecalcSize() {

                scrollcontentpos = scrollcontent.offset();
                scrollcontainerpos = scrollcontainer.offset();

                if (ap) { scrollcontainerpos.left = 0; scrollcontainerpos.top = 0; }

                if (options.verticalscrollbar) {
                    scrollcontainer.css("width", '100%');
                    scrollcontent.css("width", ''); //resets the width to whatever is in the .css

                    scrollcontainer.width(scrollcontent.width() + scrollbar.width());
                    scrollcontent.width(scrollcontainer.width() - scrollbar.width());
                    if (ap)
                        scrollbar.height((scrollcontent.height() / scrollhw) * scrollcontent.height());
                    else
                        if (scrollcontent.prop('scrollHeight') != scrollcontent.height()) scrollbar.height((scrollcontent.height() / scrollcontent.prop('scrollHeight')) * scrollcontent.height());
                    scrollbar.css({ "left": scrollcontainerpos.left + scrollcontainer.width() - scrollbar.width() + "px" });
                    if (scrollbar.height() < options.min_scrollbar_size) scrollbar.height(options.min_scrollbar_size);
                }
                else {
                    scrollcontainer.css("width", '100%');
                    scrollcontent.css("width", ''); //resets the width to whatever is in the .css

                    scrollcontainer.width(scrollcontent.width());
                    scrollcontent.width(scrollcontainer.width());
                    scrollcontainer.height(scrollcontent.height() + scrollbar.height());
                    if (ap)
                        scrollbar.width((scrollcontent.width() / scrollhw) * scrollcontent.width());
                    else
                        if (scrollcontent.prop('scrollWidth') != scrollcontent.width()) scrollbar.width((scrollcontent.width() / scrollcontent.prop('scrollWidth')) * scrollcontent.width());
                    scrollbar.css({ "top": scrollcontainer.height() - scrollbar.height() + scrollcontainerpos.top + "px" });
                    if (scrollbar.width() < options.min_scrollbar_size) scrollbar.width(options.min_scrollbar_size);
                    if (scrollbar.offset().left + scrollbar.width() > scrollcontainerpos.left + scrollcontent.width()) scrollbar.css({ "left": scrollcontainerpos.left + scrollbar.offset().left - (scrollbar.offset().left + scrollbar.width() - scrollcontent.width()) + "px" });
                    if (scrollbar.offset().left < scrollcontainerpos.left) scrollbar.css({ "left": scrollcontainerpos.left });
                }
            }

        });

    }

})(jQuery);

//helper functions

function enableSelection(target) {

    if (typeof target.onselectstart != "undefined") //IE route
        target.onselectstart = function () { return true };

    if (typeof target.style.MozUserSelect != "undefined") //Firefox route
        target.style.MozUserSelect = "text";

    if (typeof target.style.KhtmlUserSelect != "undefined") //Firefox/chrome route
        target.style.KhtmlUserSelect = "text";

    target.onmousedown = function () { return true };

}

function disableSelection(target) {

    if (typeof target.onselectstart != "undefined") //IE route
        target.onselectstart = function () { return false };

    if (typeof target.style.MozUserSelect != "undefined") //Firefox route
        target.style.MozUserSelect = "none";

    if (typeof target.style.KhtmlUserSelect != "undefined") //Firefox/chrome route
        target.style.KhtmlUserSelect = "none";

    target.onmousedown = function () { return false };

}
'''