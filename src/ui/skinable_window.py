import gtk
import gobject
import os
import pango
import cairo


class SkinableWindow(gtk.Window):


    def __init__(self, transparent=False):
        super(SkinableWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.image_path = None
        self.set_app_paintable(True)
        if transparent:
            self.set_colormap(self.get_screen().get_rgba_colormap())
        self.connect('expose-event', self._on_draw)

    def _on_draw(self, widget, event):
	return False

        if os.path.isfile(self.image_path):
            try:
                cr = widget.window.cairo_create()
                pixbuf = gtk.gdk.pixbuf_new_from_file(self.image_path)
                pixbuf_scaled = pixbuf.scale_simple(event.area.width, event.area.height, gtk.gdk.INTERP_BILINEAR)
                #widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf_scaled, 0, 0, 0,0)
                cr.set_source_pixbuf(pixbuf, 0, 0)
                del pixbuf_scaled
                del pixbuf
                cr.paint()
            except:
                pass

    def set_background_image(self, image_path):
        self.image_path = image_path

