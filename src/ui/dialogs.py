import gtk
import pango
from simple_button import SimpleButton
import gettext

gettext.install('eos-social', '/usr/share/locale', unicode=True, names=['ngettext'])


class SelectDialog(gtk.FileChooserDialog):


    def __init__(self, success_callback=None, cancel_callback=None):
        super(SelectDialog, self).__init__(
            action=gtk.FILE_CHOOSER_ACTION_OPEN, 
            buttons=(
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                gtk.STOCK_OK, gtk.RESPONSE_OK, 
                )
            )
        self._success_callback = success_callback
        self._cancel_callback = cancel_callback

    def _try_run_success_callback(self, file):
        if self._success_callback is not None:
            try:
                self._success_callback(file)
            except:
                pass

    def _try_run_cancel_callback(self):
        if self._cancel_callback is not None:
            try:
               self._cancel_callback()
            except:
               pass

    def run(self):
        response = super(SelectDialog, self).run()
        if response == gtk.RESPONSE_OK:
            file = super(SelectDialog, self).get_filename()
            if file is not None:
                self._try_run_success_callback(file)
        else:
            self._try_run_cancel_callback()

    def filter(self, name, file_types):
        filter = gtk.FileFilter()
        filter.set_name(name)
        for ft in file_types:
            filter.add_pattern(ft)
        super(SelectDialog, self).add_filter(filter)


class ErrorDialog(gtk.Dialog):

    IMG_PATH = '/usr/share/eos-social/images/'

    def __init__(self, *args, **kwargs):
        super(ErrorDialog, self).__init__(*args, **kwargs)
        color = gtk.gdk.color_parse('#222222')
        super(ErrorDialog, self).modify_bg(gtk.STATE_NORMAL, color)
        self._set_options()
        self.hbox = gtk.HBox()
        self.vbox.pack_start(self.hbox, False, False, 5)
        self.close_button = SimpleButton()
        self.close_button.show_image(self.IMG_PATH + 'cancel_button_normal.png')
        self.close_button.set_image('click', self.IMG_PATH + 'cancel_button_down.png')
        self.close_button.set_image('release', self.IMG_PATH + 'cancel_button_normal.png')
        self.close_button.set_image('enter', self.IMG_PATH + 'cancel_button_hover.png')
        self.close_button.set_image('leave', self.IMG_PATH + 'cancel_button_normal.png')
        self.close_button.connect('button-press-event', lambda w, e: self.destroy())

        self.label_h1 = gtk.Label()
        self.label_h1.set_markup(
          """<span foreground="white">""" + _('ERROR') + """</span>""")
        self.label_h1.modify_font(pango.FontDescription("sans 14"))
        self.vbox.pack_start(self.label_h1, False, False, 0)
        self.label_h2 = gtk.Label()
        self.label_h2.set_markup(
          """<span foreground="white">""" + _('There was an error in your request.') + """</span>""")
        self.label_h2.modify_font(pango.FontDescription("sans 11"))
        self.vbox.pack_start(self.label_h2, False, False, 3)
        self.label_h3 = gtk.Label()
        self.label_h3.set_markup(
          """<span foreground="white">""" + _('Please, try again.') + """</span>""")
        self.label_h3.modify_font(pango.FontDescription("sans 11"))
        self.vbox.pack_start(self.label_h3, False, False, 3)
        self.hbox.pack_end(self.close_button, False, False, 5)

    def _set_options(self):
        self.set_role("eos-non-max")
        self.set_decorated(False)
        self.set_modal(True)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_resizable(False)

    def run(self, x, y, w, h):
        self.move(x, y)
        self.set_size_request(w, h)
        self.show_all()
        super(ErrorDialog, self).run()
