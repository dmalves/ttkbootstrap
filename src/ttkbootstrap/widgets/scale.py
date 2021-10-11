from tkinter import Variable
from tkinter import Event, EventType, ttk
from ttkbootstrap.theme.theme import ThemeBuilder
from ttkbootstrap.widgets.widget import Widget
from ttkbootstrap import utility
from ttkbootstrap.constants import *

# mousewheel event constants
MOUSEWHEEL = '<MouseWheel>'
BUTTON4 = '<Button-4>'
BUTTON5 = '<Button-5>'


class Scale(Widget, ttk.Scale):
    def __init__(self, master=None, bootstyle='primary', orient=HORIZONTAL,
                 from_=0, to=100, precision=0, **kwargs):
        Widget.__init__(self, bootstyle, 'TScale', orient)
        ttk.Scale.__init__(self, master=master, orient=orient,
                           from_=from_, to=to, command=self.__on_value_change, **kwargs)

        self._precision = precision
        self.variable = Variable(value=kwargs.get('value') or 0)

        # Theme change will trigger rebuild of styles (if needed)
        self.bind('<<ThemeChanged>>', self._configure_bootstyle)

        # mousewheel binding variables
        self._increment = 0
        self._funcids = {}

    def __on_value_change(self, e):
        """"""
        if self._precision == 0:
            value = int(float(e))
        else:
            value = round(float(e), self._precision)
        self.variable.set(value)

    def _configure_bootstyle(self, *args):
        self._bootstyle = utility.normalize_style(self._bootstyle)
        self._widget_color = utility.find_widget_color(self._bootstyle)

        # create ttk style from bootstyle keywords
        utility.create_ttk_style(self)

        #  build actual ttk style if not already existing
        builder: ThemeBuilder = self._theme.theme_builder

        if not self._theme.style_exists(self._ttkstyle):
            builder.create_scale_style(self)

        # set the widget ttk style
        self.configure(style=self._ttkstyle)

    def bind_mousewheel(self, increment: int = 5):
        """Causes the mousewheel movement to change the widget value
        when the mouse is hovered over the widget and the mousewheel
        is moved.

        Parameters
        ----------
        increment : int, optional
            The amount by which the value of the widge will change when
            the mousewheel is interacted. Default = 5

        Returns
        -------
        Dict[str, str]
            A dictionary of func ids that can be used to unbind the mousewheel
            functions. It is better to handle this with the 
            `unbind_mousewheel` method rather than to handle it manually.
        """
        if self._funcids:
            return

        self._increment = increment

        self._funcids[MOUSEWHEEL] = self.bind(
            MOUSEWHEEL, self._on_mousewheel_interact)
        self._funcids[BUTTON4] = self.bind(
            BUTTON4, self._on_mousewheel_interact)
        self._funcids[BUTTON5] = self.bind(
            BUTTON5, self._on_mousewheel_interact)

        return self._funcids

    def unbind_mousewheel(self):
        """Remove the binding of the mousewheel on this widget"""
        if not self._funcids:
            return

        self.unbind(MOUSEWHEEL, self._funcids[MOUSEWHEEL])
        self.unbind(BUTTON4, self._funcids[BUTTON4])
        self.unbind(BUTTON5, self._funcids[BUTTON5])

        self._funcids.clear()

    def _on_mousewheel_interact(self, e: Event):
        """Callback for mousewheel interaction with widget"""
        min_value = self.cget('from')
        max_value = self.cget('to')
        inverted = min_value > max_value
        old_value = self.get()

        # windows / mac mouse-wheel
        if e.type == EventType.MouseWheel:
            delta = 1 if e.delta > 0 else -1

        # linux mouse-wheel
        elif e.type == EventType.ButtonPress:
            if e.num == 4:
                delta = 1
            elif e.num == 5:
                delta = -1

        # calculate new widget value
        if delta < 0:
            limit = min_value if not inverted else max_value
            new_value = int(old_value - self._increment)
            self.set(limit if new_value < limit else new_value)
        else:
            limit = max_value if not inverted else min_value
            new_value = old_value + self._increment
            self.set(limit if new_value > limit else new_value)
