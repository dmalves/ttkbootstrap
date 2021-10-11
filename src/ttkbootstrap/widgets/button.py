from tkinter import ttk
from ttkbootstrap.widgets.widget import Widget
from ttkbootstrap.theme import ThemeBuilder
from ttkbootstrap import utility
from ttkbootstrap.constants import *


class Button(Widget, ttk.Button):
    def __init__(self, master=None, bootstyle='primary', **kwargs):
        Widget.__init__(self, bootstyle, 'TButton')
        ttk.Button.__init__(self, master=master, **kwargs)
        self._funcids = {}

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
            if OUTLINE in self._bootstyle:
                builder.create_outline_button_style(self)
            elif LINK in self._bootstyle:
                builder.create_link_button_style(self)
            else:
                builder.create_button_style(self)

        # set the widget ttk style
        self.configure(style=self._ttkstyle)

    def bind_return_key(self):
        """Pressing the <Return> key will invoke the method associated 
        with the button when the button has focus."""
        sequence = '<Return>'
        if not self._funcids:
            funcid = self.bind(sequence, lambda _: self.invoke())
            self._funcids[sequence] = funcid

    def unbind_return_key(self):
        """Remove the <Return> event binding. Pressing the <Return> key 
        will not invoke the method associated with the button.
        """
        sequence = '<Return>'
        if sequence in self._funcids:
            self.unbind(sequence, self._funcids[sequence])
            self._funcids.clear()
