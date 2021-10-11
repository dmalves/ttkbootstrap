from tkinter import ttk
from ttkbootstrap.theme.theme import ThemeBuilder
from ttkbootstrap.widgets.widget import Widget
from ttkbootstrap import utility
from ttkbootstrap.constants import *


class Separator(Widget, ttk.Separator):
    def __init__(self, master=None, bootstyle=DEFAULT, orient=HORIZONTAL,
                 **kwargs):
        Widget.__init__(self, bootstyle, 'TSeparator', orient)
        ttk.Separator.__init__(self, master=master, orient=orient, **kwargs)

        # Theme change will trigger rebuild of styles (if needed)
        self.bind('<<ThemeChanged>>', self._configure_bootstyle)

    def _configure_bootstyle(self, *args):
        self._bootstyle = utility.normalize_style(self._bootstyle)
        self._widget_color = utility.find_widget_color(self._bootstyle)

        # create ttk style from bootstyle keywords
        utility.create_ttk_style(self)

        #  build actual ttk style if not already existing
        builder: ThemeBuilder = self._theme.theme_builder

        if not self._theme.style_exists(self._ttkstyle):
            builder.create_separator_style(self)

        # set the widget ttk style
        self.configure(style=self._ttkstyle)
