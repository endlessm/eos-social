import gtk


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


class SelectVideoDialog(SelectDialog):


    def __init__(self, *args, **kwargs):
        super(SelectVideoDialog, self).__init__(*args, **kwargs)

class SelectImageDialog(SelectDialog):


    def __init__(self, *args, **kwargs):
        super(SelectImageDialog, self).__init__(*args, **kwargs)

