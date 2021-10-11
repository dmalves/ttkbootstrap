import tkinter as tk
from ttkbootstrap.widgets.widget import Widget
from ttkbootstrap.constants import *


class Window(Widget, tk.Tk):

    def __init__(self, title='ttkbootstrap', theme='flatly',
                 bootstyle='default', size=None, position=None, 
                 resizable=True, minsize=None, maxsize=None, alpha=1.0,
                 topmost=False, icon=None, **kw):
        """The application window.

        Parameters
        ----------
        title : str, optional
            The window title. Default='ttkbootstrap'. This is a
            convience parameter that calls the `Tk.title` method
            internally.
        
        theme : str, optional
            The theme used when rendering the widget colors. 
            Default='flatly'.
        
        bootstyle : str, optional.
            Keywords used to control the widget style. 
            Default='default'.

        size : Tuple[int, int], optional
            The width and height of the window. This is a convenience 
            parameter that calls the `Tk.geometry` method if set.

        position : Tuple[int, int], optional
            The coordinates of the northwest corner ofthe window
            relative to the root window. This is a convience 
            parameter and calls the `Tk.geometry` method if set.
        
        resizable : bool, optional
            Controls whether the window is resizable (True) or not
            (False). This is a convenience parameter that calls the
            `Tk.resizable` method internally and assumes that both
            horizontal and vertical resizing are the same. Use the
            `resizable` method directly for more control.

        minsize : tuple[int, int], optional
            Specifies the minimum permissible size of the window. The
            default is platform dependent. This is a convenience
            parameter that calls the `Tk.maxsize` method internally.

        maxsize : tuple[int, int], optional
            Specifies the maximum permissible size of the window. The
            default is the screen size. This is a convenience parameter
            that calls the `Tk.minsize` method internally.

        alpha : float, optional
            Sets the transparency level. Accepts are floating point 
            number between 0.0 and 1.0. This is a convenience method
            that internally calls the method 
            `Tk.attributes('-transparentcolor')`.

        icon : Union[str, PhotoIcon]
            Sets the titlebar icon. This is a convenience parameter
            that calls the `Tk.iconphoto` method internally.

        """

        tk.Tk.__init__(self, **kw)
        Widget.__init__(self, bootstyle, '.')

        # Theme change will trigger rebuild of styles (if needed)
        self.bind('<<ThemeChanged>>', self._configure_bootstyle)

        # convenience paramaters
        self.__set_title(title)
        self.__set_size(size)
        self.__set_minsize(minsize)
        self.__set_maxsize(maxsize)
        self.__set_position(position)
        self.__set_icon(icon)
        self.__set_alpha(alpha)
        self.__set_topmost(topmost)
        self.__set_resizable(resizable)

        self.theme.use(theme)
        self._configure_bootstyle(self)

    @property
    def theme(self):
        return self._theme

    def _configure_bootstyle(self, _):
        self.theme.theme_builder.update_window_style(self)

    def __set_title(self, text):
        self.title(text)

    def __set_size(self, value):
        if value:
            x, y = value
            self.geometry(f'{x}x{y}')

    def __set_resizable(self, value):
        self.resizable(value, value)

    def __set_position(self, value):
        if value:
            x, y = value
            self.geometry(f'+{x}+{y}')

    def __set_minsize(self, value):
        if value:
            x, y = value
            self.minsize(x, y)

    def __set_maxsize(self, value):
        if value:
            x, y = value
            self.maxsize(x, y)

    def __set_icon(self, image):
        if image:
            self.iconphoto(True, image)

    def __set_alpha(self, amount):
        self.attributes('-alpha', amount)

    def __set_topmost(self, value):
        self.attributes('-topmost', value)
