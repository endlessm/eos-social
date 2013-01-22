import gtk


class SelectVideoDialog(gtk.FileChooserDialog):


    def __init__(self):
        super(SelectVideoDialog, self).__init__(
            action=gtk.FILE_CHOOSER_ACTION_OPEN, 
            buttons=(
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                gtk.STOCK_OK, gtk.RESPONSE_OK, 
                )
            )
        # insert filters here
