import gtk
import gobject
import os
import gettext

gettext.install('eos-social', '/usr/share/locale', unicode=True, names=['ngettext'])

class MultiPanel(gtk.Alignment):


    def __init__(self):
        super(MultiPanel, self).__init__(xalign=0.0, yalign=0.0, xscale=1.0, 
          yscale=1.0)
        self._map = {}
        self._container = gtk.VBox()
        self.add(self._container)
        self._container.hide()
        self.hide()

    def add_panel(self, panel, panel_name):
        self._map[panel_name] = panel
        self._container.pack_start(panel, expand=True, fill=True, padding=0)
        panel.hide()

    def _show_panel(self, panel):
        for current_panel in self._map.values():
            if current_panel is panel:
                current_panel.show()
            else:
                current_panel.hide()

    def show_panel(self, panel_name):
        panel = self._map.get(panel_name, None)
        if panel is not None:
            self._show_panel(panel)

    def hide_all(self):
        for current_panel in self._map.values():
            current_panel.hide()

