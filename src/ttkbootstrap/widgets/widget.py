from tkinter import ttk
from ttkbootstrap.theme.theme import Theme


class Widget:

    def __init__(self, bootstyle, widget_class, widget_orient=None):

        self._theme: Theme = next(Theme.get_instance())
        self._bootstyle = bootstyle
        self._widget_class = widget_class
        self._widget_orient = widget_orient
        self._widget_color: str = ''
        self._ttkstyle = ''

    def configure(self, option=None, **kwargs):
        if option is not None:
            if option == 'bootstyle':
                return self._bootstyle
            else:
                return ttk.Widget.configure(self, option)
        else:
            bootstyle = kwargs.get('bootstyle')
            if bootstyle is not None:
                del(kwargs['bootstyle'])
                self._bootstyle = bootstyle
                self._configure_bootstyle()
            ttk.Widget.configure(self, **kwargs)
