import gtk
import gobject
import os
import pango
import cairo


class SimpleButton(gtk.EventBox):


    def __init__(self):
        super(SimpleButton, self).__init__()
        self._image_map = {}
        self.set_visible_window(False)
        self.image = gtk.Image()
        self.add(self.image)
        self.connect('button-press-event', self._on_click)
        self.connect('button_release_event', self._on_release)
        self.connect('enter_notify_event', self._on_enter)
        self.connect('leave_notify_event', self._on_leave)
        self.set_events(gtk.gdk.EXPOSURE_MASK
                            | gtk.gdk.LEAVE_NOTIFY_MASK
                            | gtk.gdk.ENTER_NOTIFY_MASK
                            | gtk.gdk.BUTTON_PRESS_MASK
                            | gtk.gdk.BUTTON_RELEASE_MASK
                            )

    def set_image(self, image_name, image_file):
        self._image_map[image_name] = image_file

    def show_image(self, image_file):
        if image_file:
            self.image.set_from_file(image_file)

    def _on_click(self, w, e):
        self.show_image(self._image_map.get('click', None))

    def _on_release(self, w, e):
        self.show_image(self._image_map.get('release', None))

    def _on_enter(self, w, e):
        self.show_image(self._image_map.get('enter', None))

    def _on_leave(self, w, e):
        self.show_image(self._image_map.get('leave', None))

