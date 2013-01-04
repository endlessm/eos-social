#!/usr/bin/env python
import gtk
from ui import MainWindow


def main():
    win = MainWindow()
    win.connect('destroy', lambda w: gtk.main_quit())

    win.show_all()
    gtk.main()

def __on_button_press(widget, event):
    print 'press'


if __name__ == '__main__':
    main()