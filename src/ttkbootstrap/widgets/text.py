from ttkbootstrap import utility
from ttkbootstrap.constants import FOCUSFRAME
from ttkbootstrap.widgets.widget import Widget
from ttkbootstrap.widgets.scrollbar import Scrollbar
from ttkbootstrap.widgets.frame import Frame
from tkinter import Text as tkText
from tkinter import Pack, Place, Grid
from ttkbootstrap.theme.theme import ThemeBuilder
from tkinter.constants import *
from tkinter import scrolledtext

# TODO width and height are not working
# TODO padding doesn't work when not focusstyle

class Text(Widget, tkText):

    def __init__(self, master=None, bootstyle='default', focusframe=True,
                 padding=2, showscrollbar=True, **kwargs):
        Widget.__init__(self, bootstyle, 'Text')
        self.showscrollbar = showscrollbar
        self.focusframe = focusframe
        self._funcids = {}
        
        # create the widget frame
        frame_style = ''.join(self._bootstyle)
        if focusframe:
            frame_style += FOCUSFRAME

        self.container = Frame(
            master, 
            bootstyle=frame_style,
            padding=padding
        )

        # instantiate the text widget
        tkText.__init__(self, self.container, **kwargs)
        self.pack(side=LEFT, fill=BOTH, expand=YES)

        # give control of geometry manager to the container
        text_meths = vars(tkText).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.container, m))

        # setup the scrollbar
        self.scrollbar = Scrollbar(
            self.container,
            command=self.yview
        )
        self.scrollbar.pack(side=RIGHT, fill=Y, expand=YES)
        self.configure(yscrollcommand=self.scrollbar.set)
        
        # initialize the widget style
        self._configure_bootstyle(self)

        # Theme change will trigger rebuild of styles (if needed)
        self.bind('<<ThemeChanged>>', self._configure_bootstyle)

    def _configure_bootstyle(self, *args):
        self._bootstyle = utility.normalize_style(self._bootstyle)
        self._widget_color = utility.find_widget_color(self._bootstyle)

        # create ttk style from bootstyle keywords
        utility.create_ttk_style(self)

        #  build actual ttk style if not already existing
        builder: ThemeBuilder = self._theme.theme_builder
        builder.update_text_style(self)

    def hide_scrollbar(self, *args):
        """Hide the vertical scrollbar"""
        if self.scrollbar.winfo_ismapped():
            self.scrollbar.pack_forget()
            print('hiding scrollbar')

    def show_scrollbar(self, *args):
        """Show the vertical scrollbar"""
        if not self.scrollbar.winfo_ismapped():
            self.scrollbar.pack()
            print('showing scrollbar')
