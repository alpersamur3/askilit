import gi
from gi.repository import Gtk

class MessageBox(Gtk.Dialog):
    def __init__(self, title, message):
        super().__init__(title=title, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        label = Gtk.Label(label=message)
        box = self.get_content_area()
        box.add(label)
        self.show_all()

def askokcancel(title, message):
    dialog = MessageBox(title, message)
    response = dialog.run()
    dialog.destroy()
    return response == Gtk.ResponseType.OK
