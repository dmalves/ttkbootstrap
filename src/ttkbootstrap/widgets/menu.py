from tkinter import Menu as tkMenu
from ttkbootstrap.theme.theme import ThemeBuilder
from ttkbootstrap.widgets.widget import Widget
from ttkbootstrap import utility
from ttkbootstrap.constants import *

# TODO add tk menu style


class Menu(Widget, tkMenu):
    def __init__(self, master=None, bootstyle='default', **kwargs):
        Widget.__init__(self, bootstyle, 'Menu')
        tkMenu.__init__(self, master=master, **kwargs)

        # Theme change will trigger rebuild of styles (if needed)
        self.bind('<<ThemeChanged>>', self._configure_bootstyle)
        self._configure_bootstyle(self)

    def _configure_bootstyle(self, *args):
        self._bootstyle = utility.normalize_style(self._bootstyle)
        self._widget_color = utility.find_widget_color(self._bootstyle)

        # create ttk style from bootstyle keywords
        utility.create_ttk_style(self)

        #  build actual ttk style if not already existing
        builder: ThemeBuilder = self._theme.theme_builder
        builder.update_menu_style(self)
