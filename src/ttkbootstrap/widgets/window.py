import tkinter as tk
from ttkbootstrap.widgets.widget import Widget
from ttkbootstrap.constants import *


class Window(Widget, tk.Tk):

    def __init__(self, title='ttkbootstrap', theme='cosmo',
                 bootstyle='default'):

        tk.Tk.__init__(self)
        Widget.__init__(self, bootstyle, '.')

        # Theme change will trigger rebuild of styles (if needed)
        self.bind('<<ThemeChanged>>', self._configure_bootstyle)
        self.title(title)
        self.theme.use(theme)
        self._configure_bootstyle(self)

    @property
    def theme(self):
        return self._theme

    def _configure_bootstyle(self, _):
        self.theme.theme_builder.update_window_style(self)
