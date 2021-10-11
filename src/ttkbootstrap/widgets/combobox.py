from tkinter import ttk
from ttkbootstrap.theme.theme import ThemeBuilder
from ttkbootstrap.widgets.widget import Widget
from ttkbootstrap import utility
from ttkbootstrap.constants import *


class Combobox(Widget, ttk.Combobox):
    def __init__(self, master=None, bootstyle='primary',
                 scrollbarthickness=8, **kwargs):

        self._thickness = scrollbarthickness
        self._funcids = {}

        Widget.__init__(self, bootstyle, 'TCombobox')
        ttk.Combobox.__init__(self, master=master, **kwargs)

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
            builder.create_combobox_style(self, self._thickness)

        # set the widget ttk style
        self.configure(style=self._ttkstyle)

    def bind_select_command(self, func):
        """Bind the <<ComboboxSelected>> event to a function. The function 
        signature must include a parameter `e` for the event callback."""
        sequence = '<<ComboboxSelected>>'
        if sequence not in self._funcids:
            self._funcids[sequence] = self.bind(sequence, func)

    def unbind_select_command(self):
        """Unbind the <<ComboboxSelected>> event"""
        sequence = '<<ComboboxSelected>>'
        if sequence in self._funcids:
            self.unbind(sequence, self._funcids[sequence])
            del(self._funcids[sequence])
