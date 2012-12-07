#!/usr/bin/env python
import gtk
from ui import MainWindow


def main():
    win = MainWindow()
    win.connect('destroy', lambda w: gtk.main_quit())

    btn_add = gtk.Button()
    btn_add.set_size_request(64, 64)
    btn_add.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    btn_add.connect("button-press-event", __on_button_press)

    main_container = gtk.VBox()
    main_container.pack_start(btn_add, expand=False, fill=False, padding=0)
    win.add(main_container)

    win.show_all()
    gtk.main()

def __on_button_press(widget, event):
    print 'press'


if __name__ == '__main__':
    main()