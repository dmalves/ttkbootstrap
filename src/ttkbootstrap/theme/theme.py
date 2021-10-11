import re
from typing import Any, Tuple
import weakref
import colorsys
from uuid import uuid4
from PIL import Image, ImageDraw, ImageColor, ImageFont
from PIL.ImageTk import PhotoImage
from tkinter import font as tkFont
from tkinter.ttk import Style as ttk_Style
from ttkbootstrap.theme.definitions import DEFINED_THEMES
from ttkbootstrap.constants import *

# TODO add callback to change main background color on theme change for root window

COLOR_PATTERN = re.compile(r"primary|secondary|success|info|warning|danger")


class ThemeDefinition:
    """Defines the name, colors, and type of the theme."""

    def __init__(self, name, dark=False, colors=None):
        """A class to provide defined name, colors, and font settings
        for a freestyle theme.

        Parameters
        ----------
        name : str, optional
            The name of the theme. Default='default'.

        dark : bool, optional
            True if the theme is dark, otherwise False. Default=False.

        colors : Colors, optional
            An instance of the Color class containing the theme colors.
            Default=None.

        """
        self.name: str = name
        self.dark: bool = dark
        self.colors: Colors = colors

    def __repr__(self):
        return f"name={self.name}, dark={self.dark}, colors={self.colors}"

    @staticmethod
    def load_defined_themes():
        """Load all freestyle pre-defined themes.

        Returns
        -------
        dict
            Theme definitions.
        """
        definitions = dict()
        for name, settings in DEFINED_THEMES.items():
            definitions.update(
                {
                    name: ThemeDefinition(
                        name=name,
                        dark=settings["type"] == "dark",
                        colors=Colors(**settings["colors"]),
                    )
                }
            )
        return definitions


class Colors:
    """Contains theme colors and other color related methods."""

    def __init__(self, primary, secondary, success, info, warning, danger,
                 background, foreground, selectfg, selectbg, border, inputfg,
                 inputbg):
        """A class for managing theme colors.

        Parameters
        ----------
        primary : str
            The primary theme color; used by default for all widgets.

        secondary : str
            An accent color; commonly of a grey hue.

        success : str
            An accent color; commonly of a green hue.

        info : str
            An accent color; commonly of a blue hue.

        warning : str
            An accent color; commonly of an orange hue.

        danger : str
            An accent color; commonly of a red hue.

        background : str
            Background color.

        foreground : str
            Default text color.

        selectfg : str
            The color of selected text.

        selectbg : str
            The background color of selected text.

        border : str
            The color used for widget borders.

        inputfg : str
            The text color for input widgets: ie. 'Entry', 'Combobox', etc...

        inputbg : str
            The text background color for input widgets.
        """
        self.primary: str = primary
        self.secondary: str = secondary
        self.success: str = success
        self.info: str = info
        self.warning: str = warning
        self.danger: str = danger
        self.background: str = background
        self.foreground: str = foreground
        self.selectfg: str = selectfg
        self.selectbg: str = selectbg
        self.border: str = border
        self.inputfg: str = inputfg
        self.inputbg: str = inputbg

    def __iter__(self):
        return iter(
            ["primary", "secondary", "success", "info", "warning",
             "danger"])

    def __repr__(self):
        return str(self.__dict__)

    def get(self, color: str) -> str:
        """Get a color value

        Parameters
        ----------
        color : str
            The name of a color label (ie. primary, secondary, etc...)

        Returns
        -------
        str
            The value associated with the color label.
        """
        return self.__dict__.get(color)

    def set(self, color: str, value: str):
        """Set a color value

        Parameters
        ----------
        color : str
            The name of a color label (ie. primary, secondary, etc...)

        value : str
            The hexadecimal value of the color to set.
        """
        if color in self.__dict__:
            self.__dict__.update({color: value})

    @property
    def labels(self):
        """Returns an iterator of all color property labels"""
        return iter(self.__dict__.keys())

    @staticmethod
    def hex_to_rgb(color: str) -> Tuple[float, float, float]:
        """Convert hexadecimal color to rgb color value.

        Parameters
        ----------
        color : str
            The hexadecimal color value

        Returns
        -------
        Tuple[float, float, float]
            The rgb color value.
        """
        if len(color) == 4:
            # 3 digit hexadecimal colors
            r = round(int(color[1], 16) / 255, 2)
            g = round(int(color[2], 16) / 255, 2)
            b = round(int(color[3], 16) / 255, 2)
        else:
            # 6 digit hexadecimal colors
            r = round(int(color[1:3], 16) / 255, 2)
            g = round(int(color[3:5], 16) / 255, 2)
            b = round(int(color[5:], 16) / 255, 2)
        return r, g, b

    @staticmethod
    def rgb_to_hex(r: float, g: float, b: float) -> str:
        """Convert rgb to hexadecimal color value

        Parameters
        ----------
        r : float
            Red color value (between 0.0 and 1.0)

        g : float
            Green color value (between 0.0 and 1.0)

        b : float
            Blue color value (between 0.0 and 1.0)

        Returns
        -------
        str
            The hexadecimal color value
        """
        r_ = max(0, min(int(r * 255), 255))
        g_ = max(0, min(int(g * 255), 255))
        b_ = max(0, min(int(b * 255), 255))
        return "#{:02x}{:02x}{:02x}".format(r_, g_, b_)

    @staticmethod
    def normalize(color, fallback, theme_colors=None) -> str:
        """Standard colors by converting to its hex value.

        Parameters
        ----------
        color : str
            The color to normalize.

        fallback : str
            The fallback color if the conversion fails.

        theme_colors : Colors, optional.
            A theme's color object. Default=None.

            Returns:
            str: a hex color value.
        """
        if not color:
            return fallback

        if "#" in color:
            return color

        style_color = re.search(COLOR_PATTERN, color)
        if style_color and theme_colors:
            return theme_colors.get(color)

        if "#" not in color:
            rgb = [round(x / 255, 2) for x in ImageColor.getrgb(color)]
            return Colors.rgb_to_hex(*rgb)

        return fallback

    @staticmethod
    def update_hsv(color, hd=0, sd=0, vd=0):
        """Modify the hue, saturation, and/or value of a given hex
        color value.

        Parameters
        ----------
        color : str
            The hexadecimal color value that is the target of hsv
            changes.

        hd : float, optional
            % change in hue. Default=0.

        sd : float, optional
            % change in saturation, Default=0.

        vd : float, optional
            % change in value, Default=0.

        Returns
        -------
        str
            A new hexadecimal color value that results from the hsv
            arguments passed into the function.
        """
        r, g, b = [round(x / 255, 2) for x in ImageColor.getrgb(color)]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # hue
        if h * (1 + hd) > 1:
            h = 1
        elif h * (1 + hd) < 0:
            h = 0
        else:
            h *= 1 + hd

        # saturation
        if s * (1 + sd) > 1:
            s = 1
        elif s * (1 + sd) < 0:
            s = 0
        else:
            s *= 1 + sd

        # value
        if v * (1 + vd) > 1:
            v = 0.95
        elif v * (1 + vd) < 0.05:
            v = 0.05
        else:
            v *= 1 + vd

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Colors.rgb_to_hex(r, g, b)


class Theme:
    """Create and manage the application widget styles."""

    _instances = set()

    def __init__(self, master=None, theme_name='flatly', theme_builder=None):
        self._instances.add(weakref.ref(self))
        self.ttkstyle: ttk_Style = ttk_Style(master=master)
        self.defined_themes: dict = ThemeDefinition.load_defined_themes()
        self.definition: ThemeDefinition = None

        # set theme builder
        if theme_builder is None:
            self.theme_builder = ThemeBuilder(self)
        else:
            self.theme_builder = theme_builder(self)

        self._assets = dict()  # image container for widget layouts
        self._registry = dict()  # track built ttk styles

        # get theme definition
        if theme_name in self.defined_themes:
            self.definition = self.get_definition(theme_name)

        # create initial ttk theme
        self.create(theme_name)

    @classmethod
    def get_instance(cls):
        dead = set()
        if len(cls._instances) == 0:
            yield Theme()
        else:
            for ref in cls._instances:
                obj = ref()
                if obj is not None:
                    yield obj
                else:
                    dead.add(ref)
            cls._instances -= dead

    @property
    def colors(self) -> Colors:
        """The colors used to build the active theme

        Color Attributes
        ----------------
        - primary
        - secondary
        - success
        - info
        - warning
        - danger
        - bg
        - fg
        - selectfg
        - selectbg
        - border
        - inputfg
        - inputbg

        """
        return self.definition.colors

    @property
    def name(self):
        """The name of the active theme."""
        return self.definition.name

    @property
    def is_dark_theme(self) -> bool:
        """Returns True if the theme is dark, otherwise False."""
        return self.definition.dark

    @property
    def is_light_theme(self) -> bool:
        """Returns True if the theme is light, otherwise False."""
        return not self.definition.dark

    def theme_names(self):
        """Return a list of a defined themes"""
        return sorted(DEFINED_THEMES.keys())

    def use(self, theme_name: str):
        """Change the theme to 'theme_name'

        Parameters
        ----------
        theme_name : str
            The name of the theme.
        """
        self.definition = self.get_definition(theme_name)

        # create new theme if it doesn't already exist
        if theme_name not in self.ttkstyle.theme_names():
            self.create(theme_name)

        # change application theme
        self.ttkstyle.theme_use(theme_name)

    def get_definition(self, theme_name: str) -> ThemeDefinition:
        """Get the definition for the requested theme

        Parameters
        ----------
        theme_name : str
            The name of the theme.

        Returns
        -------
        ThemeDefinition
            The definition for the requested theme.
        """
        return self.defined_themes.get(theme_name)

    def update_theme_settings(self, settings):
        """Update the settings for the active theme; generates a
        <<ThemeChanged>> virtual event.

        Parameters
        ----------
        settings : dict
            A dictionary of theme settings created by the ThemeBuilder.
        """
        self.ttkstyle.theme_settings(self.name, settings)

    def create(self, theme_name):
        """Create a new theme if not existing.

        The theme is created with a 'clam' theme base with no
        predefined settings.

        Parameters
        ----------
        theme_name : str
            The name of the theme to create.
        """
        self.ttkstyle.theme_create(theme_name, "clam", {})
        self._registry[theme_name] = []

    def register_style(self, style):
        """Add a style to the registry for the current theme.

        Parameters
        ----------
        style : str
            The name of the ttk style.
        """
        self._registry[self.name].append(style)

    def style_exists(self, style):
        """Check if a style exists for the current theme.

        Returns
        -------
        bool
            Does the style exist?
        """
        styles = self._registry[self.name]
        return style in styles

    def register_assets(self, assets: dict):
        """Add theme assets to an assets dictionary

        This asset registry is used primary to store theme assets
        created by the ThemeBuilder object. However, it may also be
        used to store assets used in the application such as images,
        sounds, etc...

        Parameters
        ----------
        assets : dict
            A dictionary of assets to register.
        """
        self._assets.update(assets)

    def retrieve_asset(self, key: str) -> Any:
        """Retreive a theme asset stored with the 'register_assets' method.

        Parameters
        ----------
        key : str
            The name given to the asset when registered.

        Returns
        -------
        Any
            The asset that was registered.
        """
        return self._assets.get(key)


class ThemeBuilder:
    def __init__(self, theme):
        self.theme: Theme = theme

    def create_button_style(self, widget):
        """Create a button style"""
        colors = self.theme.colors
        widgetfont = 'TkDefaultFont'

        # style colors
        foreground = colors.selectfg
        focuscolor = foreground
        background = colors.get(widget._widget_color) or colors.primary
        disabledfg = colors.inputfg

        if self.theme.is_light_theme:
            pressed = Colors.update_hsv(background, vd=-0.2)
            hover = Colors.update_hsv(background, vd=-0.1)
            disabledbg = Colors.update_hsv(colors.inputfg, vd=-0.2)
        else:
            pressed = Colors.update_hsv(background, vd=0.2)
            hover = Colors.update_hsv(background, vd=0.1)
            disabledbg = Colors.update_hsv(colors.inputfg, vd=-0.3)

        # build widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=background,
            darkcolor=background,
            lightcolor=background,
            relief=RAISED,
            font=widgetfont,
            focusthickness=0,
            focuscolor=focuscolor,
            padding=5,
            width=-11,
            anchor=CENTER
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[('disabled', disabledfg)],
            background=[
                ('disabled', disabledbg),
                ('pressed', pressed),
                ('hover', hover)
            ],
            bordercolor=[
                ('disabled', disabledbg),
                ('hover !disabled', hover)
            ],
            darkcolor=[
                ('disabled', disabledbg),
                ('pressed !disabled', pressed),
                ('hover !disabled', hover)
            ],
            lightcolor=[
                ('disabled', disabledbg),
                ('pressed !disabled', pressed),
                ('hover !disabled', hover)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_outline_button_style(self, widget):
        colors = self.theme.colors
        widgetfont = 'TkDefaultFont'

        # style colors
        foreground = colors.get(widget._widget_color) or colors.primary
        focuscolor = foreground
        background = colors.background
        selectfg = colors.selectfg

        if self.theme.is_light_theme:
            pressed = Colors.update_hsv(foreground, vd=-0.1)
            disabledfg = Colors.update_hsv(colors.inputbg, vd=-0.2)
        else:
            pressed = Colors.update_hsv(foreground, vd=0.1)
            disabledfg = Colors.update_hsv(colors.inputbg, vd=-0.3)

        # build widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=foreground,
            darkcolor=background,
            lightcolor=background,
            relief=RAISED,
            font=widgetfont,
            focusthickness=0,
            focuscolor=focuscolor,
            padding=5,
            width=-11,
            anchor=CENTER
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[
                ('disabled', disabledfg),
                ('pressed', selectfg),
                ('hover', selectfg)
            ],
            focuscolor=[
                ('pressed', selectfg),
                ('hover', selectfg),
            ],
            background=[
                ('pressed !disabled', pressed),
                ('hover !disabled', foreground)
            ],
            bordercolor=[
                ('pressed !disabled', pressed),
                ('hover !disabled', foreground)
            ],
            darkcolor=[
                ('pressed !disabled', pressed),
                ('hover !disabled', foreground)
            ],
            lightcolor=[
                ('pressed !disabled', pressed),
                ('hover !disabled', foreground)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_link_button_style(self, widget):
        colors = self.theme.colors
        widgetfont = 'TkDefaultFont'

        # style colors
        foreground = colors.get(widget._widget_color) or colors.primary
        focuscolor = foreground
        background = colors.background

        if self.theme.is_light_theme:
            disabledfg = Colors.update_hsv(colors.inputbg, vd=-0.2)
        else:
            disabledfg = Colors.update_hsv(colors.inputbg, vd=-0.3)

        # build widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=background,
            darkcolor=background,
            lightcolor=background,
            relief=RAISED,
            font=widgetfont,
            focusthickness=0,
            focuscolor=focuscolor,
            padding=5,
            width=-11,
            anchor=CENTER
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[
                ('disabled', disabledfg),
                ('pressed !disabled', colors.info),
                ('hover !disabled', colors.info)
            ],
            shiftrelief=[('pressed !disabled', -1)],
            background=[],
            bordercolor=[],
            darkcolor=[],
            lightcolor=[]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_checkbutton_assets(self, indicatorcolor, element,
                                  checksettings):
        fontname, fontsize, fontoffset = checksettings
        checkfont = ImageFont.truetype(fontname, fontsize)

        # TODO refactor image creation to single inner function

        # check colors
        colors = self.theme.colors
        outline = colors.border

        if self.theme.is_light_theme:
            fill = colors.inputbg
            disabledfg = Colors.update_hsv(colors.inputbg, vd=-0.2)
            disabledbg = colors.inputbg
        else:
            fill = colors.selectbg
            disabledfg = Colors.update_hsv(colors.inputbg, vd=-0.3)
            disabledbg = colors.selectbg

        # checkbutton off
        cboff = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(cboff)
        draw.rounded_rectangle(xy=[2, 2, 132, 132], radius=16,
                               outline=outline, width=3, fill=fill)

        # checkbutton on
        cbon = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(cbon)
        draw.rounded_rectangle(xy=[2, 2, 132, 132], radius=16,
                               outline=indicatorcolor, width=3,
                               fill=indicatorcolor)

        draw.text((20, fontoffset), "✓", font=checkfont, fill=colors.selectfg)

        # checkbutton disabled
        cbdisabled = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(cbdisabled)
        draw.rounded_rectangle(xy=[2, 2, 132, 132], radius=16,
                               outline=disabledfg, width=3, fill=disabledbg)

        off_photoimage = PhotoImage(cboff.resize((14, 14)), Image.LANCZOS)
        on_photoimage = PhotoImage(cbon.resize((14, 14)), Image.LANCZOS)
        disabled_photoimage = PhotoImage(
            cbdisabled.resize((14, 14)), Image.LANCZOS)

        # save images
        self.theme.register_assets(
            {
                f"{element}.off": off_photoimage,
                f"{element}.on": on_photoimage,
                f"{element}.disabled": disabled_photoimage,
            }
        )
        return off_photoimage, on_photoimage, disabled_photoimage

    def create_checkbutton_style(self, widget):
        colors = self.theme.colors
        widgetfont = 'TkDefaultFont'
        winsys = widget._windowingsystem

        # set platform specific checkfont
        if winsys == 'win32':
            checksettings = ('seguisym.ttf', 120, -20)
        elif winsys == 'x11':
            checksettings = ('FreeSerif.ttf', 130, 10)
        else:
            checksettings = ('LucidaGrande.ttc', 120, -10)

        # style colors
        background = colors.background
        foreground = colors.foreground
        indicatorcolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            disabled = colors.border
        else:
            disabled = colors.selectbg

        # create widget assets
        element = uuid4()
        cboff, cbon, cbdisabled = self.create_checkbutton_assets(
            indicatorcolor, element, checksettings)

        # create widget style
        self.theme.ttkstyle.element_create(
            f'{element}.Checkbutton.indicator', 'image', cboff,
            ('disabled', cbdisabled),
            ('selected', cbon),
            width=20, border=4, sticky=W
        )
        self.theme.ttkstyle.layout(
            widget._ttkstyle,
            [("Checkbutton.padding",
                {"children": [
                    (f"{element}.Checkbutton.indicator",
                     {"side": LEFT, "sticky": ""}),
                    ("Checkbutton.focus", {"children": [
                        ("Checkbutton.label",
                         {"sticky": NSEW})], "side": LEFT, "sticky": ""})],
                 "sticky": NSEW})]
        )
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            background=background,
            foreground=foreground,
            focuscolor='',
            font=widgetfont,
            padding=2
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[
                ('disabled', disabled),
                ('active', Colors.update_hsv(indicatorcolor, vd=-0.2))]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_rounded_toggle_assets(self, indicatorcolor, element):

        indicator_size = (226, 130)
        x, y = indicator_size

        # widget colors
        colors = self.theme.colors
        fill = colors.background
        indicatoron = colors.selectfg

        if self.theme.is_light_theme:
            outline = colors.border
            indicatoroff = colors.border
            disabled = Colors.update_hsv(colors.inputbg, vd=-0.2)
        else:
            outline = colors.selectbg
            indicatoroff = colors.selectbg
            disabled = colors.selectbg

        def create_toggle(name, fill, outline, indicatorcolor):
            img = Image.new('RGBA', indicator_size)
            draw = ImageDraw.Draw(img)
            xy_1 = [1, 1, x-1, y-1]
            xy_2 = [18, 18, y-20, y-20]
            draw.rounded_rectangle(xy_1, 64, fill, outline, width=6)
            draw.ellipse(xy_2, indicatorcolor)
            if name == 'on':
                img = img.transpose(Image.ROTATE_180)
            photoimage = PhotoImage(img.resize((24, 15), Image.LANCZOS))
            self.theme.register_assets({f'{element}.{name}': photoimage})
            return photoimage

        disabled_image = create_toggle('disabled', fill, disabled, disabled)
        off_image = create_toggle('off', fill, outline, indicatoroff)
        on_image = create_toggle('on', indicatorcolor,
                                 indicatorcolor, indicatoron)

        return on_image, off_image, disabled_image

    def create_rounded_toggle_style(self, widget):
        colors = self.theme.colors
        widgetfont = 'TkDefaultFont'

        # style colors
        background = colors.background
        foreground = colors.foreground
        indicatorcolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            disabled = colors.border
        else:
            disabled = colors.selectbg

        # create widget assets
        element = uuid4()
        images = self.create_rounded_toggle_assets(indicatorcolor, element)

        # create widget style
        # 0-off, 1-on, 2-disabled
        self.theme.ttkstyle.element_create(
            f'{element}.Rounded.Toggle.Toolbutton.indicator', 'image', images[0],
            ('disabled', images[2]), ('!selected', images[1]),
            width=28, border=4, sticky=W
        )
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            background=background,
            foreground=foreground,
            borderwidth=0,
            relief=FLAT,
            padding=0,
            font=widgetfont
        )
        self.theme.ttkstyle.layout(
            widget._ttkstyle,
            [("Toolbutton.border",
                {"sticky": NSEW, "children": [
                    ("Toolbutton.padding", {"sticky": NSEW, "children": [
                        (f"{element}.Rounded.Toggle.Toolbutton.indicator",
                         {"side": LEFT}),
                        ("Toolbutton.label", {"side": LEFT})]})]})]
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[
                ('disabled', disabled),
                ('hover', indicatorcolor)
            ],
            background=[
                ('selected', background),
                ('!selected', background)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_squared_toggle_assets(self, indicatorcolor, element):

        indicator_size = (226, 130)
        x, y = indicator_size

        def create_button(name, boxfill, outline, indicatorfill):
            img = Image.new('RGBA', (x, y))
            draw = ImageDraw.Draw(img)
            xy_1 = [1, 1, x-1, y-1]
            xy_2 = [18, 18, y-20, y-20]
            draw.rectangle(xy_1, fill=boxfill, outline=outline, width=6)
            draw.rectangle(xy_2, indicatorfill)
            if name == 'on':
                img = img.transpose(Image.ROTATE_180)
            photoimage = PhotoImage(img.resize((24, 15), Image.LANCZOS))
            self.theme.register_assets({f'{element}.{name}': photoimage})
            return photoimage

        # element colors
        colors = self.theme.colors
        fill = colors.background

        if self.theme.is_light_theme:
            outline = colors.border
            indicatoroff = colors.border
            disabled = Colors.update_hsv(colors.inputbg, vd=-0.2)
        else:
            outline = colors.selectbg
            indicatoroff = colors.selectbg
            disabled = colors.selectbg

        off_image = create_button('off', fill, outline, indicatoroff)
        on_image = create_button('on', fill, indicatorcolor, indicatorcolor)
        disabled_image = create_button('disabled', fill, disabled, disabled)

        return on_image, off_image, disabled_image

    def create_squared_toggle_style(self, widget):
        colors = self.theme.colors
        widgetfont = 'TkDefaultFont'

        # style colors
        background = colors.background
        foreground = colors.foreground
        indicatorcolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            disabled = colors.border
        else:
            disabled = colors.selectbg

        # create widget assets
        element = uuid4()
        images = self.create_squared_toggle_assets(indicatorcolor, element)

        # create widget style
        # 0-off, 1-on, 2-disabled
        self.theme.ttkstyle.element_create(
            f'{element}.Squared.Toggle.Toolbutton.indicator', 'image', images[0],
            ('disabled', images[2]), ('!selected', images[1]),
            width=28, border=4, sticky=W
        )
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            background=background,
            foreground=foreground,
            borderwidth=0,
            relief=FLAT,
            padding=0,
            font=widgetfont
        )
        self.theme.ttkstyle.layout(
            widget._ttkstyle,
            [("Toolbutton.border", {"sticky": NSEW, "children": [
                ("Toolbutton.padding", {"sticky": NSEW, "children": [
                    (f"{element}.Squared.Toggle.Toolbutton.indicator", {"side": LEFT}),
                    ("Toolbutton.label", {"side": LEFT})]})]})]
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[
                ('disabled', disabled),
                ('hover', indicatorcolor)
            ],
            background=[
                ('selected', background),
                ('!selected', background)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_toolbutton_style(self, widget):
        colors = self.theme.colors
        widgetfont = 'TkDefaultFont'

        # style colors
        indicatorcolor = colors.get(widget._widget_color) or colors.primary
        foreground = colors.selectfg
        backgroundon = indicatorcolor
        backgroundoff = Colors.update_hsv(backgroundon, sd=-0.5, vd=0.1)
        disabledfg = colors.inputfg

        if self.theme.is_light_theme:
            disabledbg = Colors.update_hsv(colors.inputbg, vd=-0.2)
        else:
            disabledbg = Colors.update_hsv(colors.inputbg, vd=-0.3)

        # create widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            foreground=foreground,
            background=backgroundoff,
            bordercolor=backgroundoff,
            darkcolor=backgroundoff,
            lightcolor=backgroundoff,
            relief=RAISED,
            font=widgetfont,
            focusthickness=0,
            focuscolor='',
            padding=2
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[
                ('disabled', disabledfg),
            ],
            background=[
                ('disabled', disabledbg),
                ('pressed', backgroundon),
                ('selected', backgroundon),
                ('hover', backgroundon)
            ],
            bordercolor=[
                ('disabled', disabledbg),
                ('pressed', backgroundon),
                ('selected', backgroundon),
                ('hover', backgroundon)
            ],
            darkcolor=[
                ('disabled', disabledbg),
                ('pressed', backgroundon),
                ('selected', backgroundon),
                ('hover', backgroundon)
            ],
            lightcolor=[
                ('disabled', disabledbg),
                ('pressed', backgroundon),
                ('selected', backgroundon),
                ('hover', backgroundon)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_outline_toolbutton_style(self, widget):
        colors = self.theme.colors
        widgetfont = 'TkDefaultFont'

        # style colors
        colors = self.theme.colors
        backgroundon = colors.get(widget._widget_color) or colors.primary
        backgroundoff = colors.background
        indicatorcolor = backgroundon
        backgroundover = Colors.update_hsv(backgroundon, vd=-0.1)
        foregroundoff = indicatorcolor
        foregroundon = backgroundoff

        if self.theme.is_light_theme:
            disabledfg = Colors.update_hsv(colors.inputbg, vd=-0.2)
        else:
            disabledfg = Colors.update_hsv(colors.inputbg, vd=-0.3)

        # create widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            foreground=foregroundoff,
            background=backgroundoff,
            bordercolor=colors.border,
            darkcolor=backgroundoff,
            lightcolor=backgroundoff,
            relief=RAISED,
            font=widgetfont,
            focusthickness=0,
            focuscolor='',
            padding=2
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[
                ('disabled', disabledfg),
                ('pressed', foregroundon),
                ('selected', foregroundon),
                ('hover', foregroundon)
            ],
            background=[
                ('pressed', backgroundover),
                ('selected', backgroundover),
                ('hover', backgroundon)
            ],
            bordercolor=[
                ('disabled', disabledfg),
                ('pressed', backgroundover),
                ('selected', backgroundover),
                ('hover', backgroundon)
            ],
            darkcolor=[
                ('pressed', backgroundover),
                ('selected', backgroundover),
                ('hover', backgroundon)
            ],
            lightcolor=[
                ('pressed', backgroundover),
                ('selected', backgroundover),
                ('hover', backgroundon)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_combobox_scrollbar_style(self, widget, ttkstyle, thickness):
        # style colors
        colors = self.theme.colors
        troughcolor = Colors.update_hsv(colors.background, vd=0.2)
        bordercolor = troughcolor
        background = colors.inputbg

        if self.theme.is_light_theme:
            thumbcolor = Colors.update_hsv(colors.background, vd=-0.25)
        else:
            thumbcolor = Colors.update_hsv(colors.selectbg, vd=0.35, sd=-0.1)

        # create scrollbar assets
        # 0-normal, 1-pressed, 2-active, 3-trough
        element = uuid4()
        images = self.create_scrollbar_assets(
            thumbcolor, troughcolor, bordercolor, VERTICAL, element, thickness)

        # create widget style
        self.theme.ttkstyle.element_create(
            f'{element}.thumb', 'image', images[0],
            ('pressed', images[1]), ('active', images[2]),
            border=(0, thickness-3),
            sticky=NS,
            width=thickness
        )
        self.theme.ttkstyle.element_create(
            f'{element}.trough', 'image', images[3],
            border=(0, thickness-3),
            padding=0,
            width=thickness+2
        )
        self.theme.ttkstyle.configure(widget._ttkstyle, background=background)
        self.theme.ttkstyle.layout(
            ttkstyle,
            [(f"{element}.trough", {"sticky": NS, "children": [
                (f"{element}.thumb", {"expand": YES})]})])

        self.theme.register_style(ttkstyle)

    def update_combobox_popdown_style(self, widget, thickness):

        # widget colors
        colors = self.theme.colors
        selectbg = colors.get(widget._widget_color) or colors.primary

        # popdown window
        popdown_settings = {}
        popdown_settings.update(
            borderwidth=0,
            highlightthickness=3,
            highlightcolor=colors.inputbg,
            background=colors.inputbg,
            foreground=colors.inputfg,
            selectbackground=selectbg,
            selectforeground=colors.selectfg,
            font='TkDefaultFont'
        )
        settings = []
        for k, v in popdown_settings.items():
            settings.extend([f'-{k}', v])
        popdown = widget.tk.eval(f'ttk::combobox::PopdownWindow {widget}')
        widget.tk.call(f'{popdown}.f.l', 'configure', *settings)

        # popdown scrollbar
        ttkstyle = 'TCombobox.Vertical.TScrollbar'
        self.create_combobox_scrollbar_style(widget, ttkstyle, thickness)
        widget.tk.call(f'{popdown}.f.sb', 'configure', '-style', ttkstyle)

    def create_combobox_style(self, widget, thickness):

        # style colors
        colors = self.theme.colors
        background = colors.inputbg
        foreground = colors.inputfg
        focuscolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            disabledfg = Colors.update_hsv(foreground, vd=-0.2)
            bordercolor = colors.border
        else:
            disabledfg = Colors.update_hsv(foreground, vd=-0.3)
            bordercolor = colors.selectbg

        # build ttk widget style
        element = uuid4()
        self.update_combobox_popdown_style(widget, thickness)
        self.theme.ttkstyle.element_create(
            f'{element}.Combobox.downarrow', 'from', 'default'
        )
        self.theme.ttkstyle.configure(
            'ComboboxPopdownFrame',
            relief=FLAT,
            borderwidth=0,
            background=bordercolor
        )
        self.theme.ttkstyle.layout(
            widget._ttkstyle,
            [(f"{element}.Spinbox.field", {"side": TOP, "sticky": EW, "children": [
                (f"{element}.Combobox.downarrow",
                 {"side": RIGHT, "sticky": NS}),
                ("Combobox.padding", {"expand": YES, "sticky": NSEW, "children": [
                    ("Combobox.textarea", {"sticky": NSEW})]})]})]
        )
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            bordercolor=bordercolor,
            darkcolor=background,
            lightcolor=background,
            arrowcolor=foreground,
            foreground=foreground,
            fieldbackground=background,
            insertcolor=foreground,
            background=background,
            relief=FLAT,
            padding=5,
            arrowsize=12,
            insertwidth=1,
            selectbackground=colors.selectbg,
            selectforeground=colors.selectfg
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[('disabled', disabledfg)],
            bordercolor=[
                ('focus !disabled', focuscolor or bordercolor),
                ('hover !disabled', focuscolor or bordercolor),
            ],
            arrowcolor=[
                ('disabled', disabledfg),
                ('pressed !disabled', background),
                ('focus !disabled', focuscolor or bordercolor),
                ('hover !disabled', focuscolor or bordercolor)
            ],
            # lightcolor=[
            #     ('focus !disabled', focuscolor or background),
            #     ('hover !disabled', background)
            # ],
            # darkcolor=[
            #     ('focus !disabled', focuscolor or background),
            #     ('hover !disabled', background)
            # ],
        )
        self.theme.register_style(widget._ttkstyle)

    def create_entry_style(self, widget):

        # style colors
        colors = self.theme.colors
        background = colors.inputbg
        foreground = colors.inputfg
        focuscolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            disabledfg = Colors.update_hsv(foreground, vd=-0.2)
            bordercolor = colors.border
        else:
            disabledfg = Colors.update_hsv(foreground, vd=-0.3)
            bordercolor = colors.selectbg

        # build widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            bordercolor=bordercolor,
            darkcolor=background,
            lightcolor=background,
            foreground=foreground,
            fieldbackground=background,
            insertcolor=foreground,
            background=background,
            relief=FLAT,
            padding=5,
            insertwidth=1,
            selectbackground=colors.selectbg,
            selectforeground=colors.selectfg
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[('disabled', disabledfg)],
            bordercolor=[
                ('focus !disabled', focuscolor or bordercolor),
                ('hover !disabled', focuscolor or bordercolor)
            ],
            # lightcolor=[
            #     ('focus !disabled', focuscolor or background),
            #     ('hover !disabled', background)
            # ],
            # darkcolor=[
            #     ('focus !disabled', focuscolor or background),
            #     ('hover !disabled', background)
            # ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_frame_style(self, widget):
        # widget colors
        colors = self.theme.colors
        background = colors.get(widget._widget_color) or colors.background

        # build widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            background=background
        )

    def create_focusframe_style(self, widget):
        # widget colors
        colors = self.theme.colors
        background = colors.inputbg
        focuscolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            bordercolor = colors.border
        else:
            bordercolor = colors.selectbg

        # create widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            borderwidth=1,
            relief=RAISED,
            background=background,
            bordercolor=bordercolor,
            lightcolor=background,
            darkcolor=background
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            bordercolor=[
                ('focus !disabled', focuscolor),
                ('hover !disabled', focuscolor)
            ],
            lightcolor=[
                ('focus !disabled', focuscolor),
                ('hover !disabled', background)
            ],
            darkcolor=[
                ('focus !disabled', focuscolor),
                ('hover !disabled', background)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_label_style(self, widget):
        # widget colors
        colors = self.theme.colors
        background = colors.background
        foreground = colors.get(widget._widget_color) or colors.foreground

        # build widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            foreground=foreground,
            background=background
        )
        self.theme.register_style(widget._ttkstyle)

    def create_inverse_label_style(self, widget):
        # widget colors
        colors = self.theme.colors
        background = colors.get(widget._widget_color) or colors.foreground
        foreground = colors.background

        # build widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            foreground=foreground,
            background=background
        )
        self.theme.register_style(widget._ttkstyle)

    def create_labelframe_style(self, widget):
        font = 'TkDefaultFont'

        # widget colors
        colors = self.theme.colors
        background = colors.background
        foreground = colors.get(widget._widget_color) or colors.foreground

        if self.theme.is_light_theme:
            bordercolor = colors.border
        else:
            bordercolor = colors.selectbg

        # create widget style
        self.theme.ttkstyle.configure(
            f'{widget._ttkstyle}.Label',
            foreground=foreground,
            background=background,
            font=font
        )
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            relief=RAISED,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=background,
            darkcolor=background,
            background=background
        )
        self.theme.register_style(widget._ttkstyle)

    def create_listbox_style(self, widget):
        # widget colors
        colors = self.theme.colors
        background = colors.inputbg
        foreground = colors.inputfg
        focuscolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            disabledfg = colors.update_hsv(foreground, vd=-0.2)
            bordercolor = colors.border
        else:
            disabledfg = colors.update_hsv(foreground, vd=-0.3)
            bordercolor = colors.selectbg

        # create widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            background=background,
            fieldbackground=background,
            foreground=foreground,
            bordercolor=bordercolor,
            lightcolor=background,
            font='TkTextFont',
            borderwidth=2,
            padding=0,
            rowheight=20
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            background=[('selected', colors.selectbg)],
            foreground=[
                ('disabled', disabledfg),
                ('selected', colors.selectfg)
            ],
            bordercolor=[
                ('focus', focuscolor),
                ('hover', focuscolor)
            ]
            # lightcolor=[('focus', focuscolor)],
        )
        self.theme.register_style(widget._ttkstyle)

    def update_menu_style(self, widget):
        # widget colors
        colors = self.theme.colors
        background = colors.background
        foreground = colors.get(widget._widget_color) or colors.foreground

        # build widget style
        widget.configure(
            tearoff=False,
            font='TkMenuFont',
            background=background,
            foreground=foreground,
            activebackground=colors.selectbg,
            activeforeground=colors.selectfg,
            selectcolor=colors.foreground,
            relief=FLAT,
            activeborderwidth=0
        )

    def create_menubutton_style(self, widget):
        arrowsize = 3
        font = 'TkDefaultFont'

        # style colors
        colors = self.theme.colors
        disabledfg = colors.inputfg
        foreground = colors.selectfg
        background = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            disabledbg = colors.update_hsv(colors.inputbg, vd=-0.2)
            pressed = colors.update_hsv(background, vd=-0.2)
            hover = colors.update_hsv(background, vd=-0.1)
        else:
            disabledbg = colors.update_hsv(colors.inputbg, vd=-0.3)
            pressed = colors.update_hsv(background, vd=0.2)
            hover = colors.update_hsv(background, vd=0.1)

        # create widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            arrowsize=arrowsize,
            arrowcolor=foreground,
            arrowpadding=(0, 0, 15, 0),
            background=background,
            bordercolor=background,
            darkcolor=background,
            foreground=foreground,
            lightcolor=background,
            font=font,
            focusthickness=0,
            focuscolor='',  # TODO add focus ring?
            padding=5,
            width=-11,
            relief=RAISED
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            arrowcolor=[('disabled', disabledfg)],
            foreground=[('disabled', disabledfg)],
            background=[
                ('disabled', disabledbg),
                ('pressed !disabled', pressed),
                ('hover !disabled', hover)
            ],
            bordercolor=[
                ('disabled', disabledbg),
                ('hover !disabled', hover)
            ],
            darkcolor=[
                ('disabled', disabledbg),
                ('pressed !disabled', pressed),
                ('hover !disabled', hover)
            ],
            lightcolor=[
                ('disabled', disabledbg),
                ('pressed !disabled', pressed),
                ('hover !disabled', hover)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_outline_menubutton_style(self, widget):
        arrowsize = 3
        font = 'TkDefaultFont'

        # style colors
        colors = self.theme.colors
        background = colors.background
        foreground = colors.get(widget._widget_color) or colors.primary
        disabledfg = colors.selectfg

        if self.theme.is_light_theme:
            pressed = colors.update_hsv(foreground, vd=-0.2)
            hover = colors.update_hsv(foreground, vd=-0.1)
            disabledbg = colors.update_hsv(colors.inputbg, vd=-0.2)
        else:
            pressed = colors.update_hsv(foreground, vd=0.2)
            hover = colors.update_hsv(foreground, vd=0.1)
            disabledbg = colors.update_hsv(colors.inputbg, vd=-0.3)

        # create widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            arrowsize=arrowsize,
            arrowcolor=foreground,
            arrowpadding=(0, 0, 15, 0),
            background=background,
            bordercolor=foreground,
            darkcolor=background,
            foreground=foreground,
            lightcolor=background,
            font=font,
            focusthickness=0,
            focuscolor='',  # TODO add focus ring?
            padding=5,
            width=-11,
            relief=RAISED
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            arrowcolor=[
                ('disabled', disabledfg),
                ('hover', colors.selectfg)
            ],
            foreground=[
                ('disabled', disabledfg),
                ('hover', colors.selectfg)],
            background=[
                ('disabled', disabledbg),
                ('pressed !disabled', pressed),
                ('hover !disabled', hover)
            ],
            bordercolor=[
                ('disabled', disabledbg),
                ('hover !disabled', hover)
            ],
            darkcolor=[
                ('disabled', disabledbg),
                ('pressed !disabled', pressed),
                ('hover !disabled', hover)
            ],
            lightcolor=[
                ('disabled', disabledbg),
                ('pressed !disabled', pressed),
                ('hover !disabled', hover)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_notebook_style(self, widget):
        widgetfont = 'TkDefaultFont'

        # widget colors
        colors = self.theme.colors

        if self.theme.is_light_theme:
            bordercolor = colors.border
            foreground = colors.inputfg
        else:
            bordercolor = colors.selectbg
            foreground = colors.selectfg

        if not widget._widget_color:
            background = colors.inputbg
            selectfg = colors.foreground
        else:
            selectfg = colors.selectfg
            background = colors.get(widget._widget_color)

        # create widget style
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            background=colors.background,
            bordercolor=bordercolor,
            lightcolor=colors.background,
            darkcolor=colors.background,
            tabmargins=(0, 1, 1, 0),
        )
        self.theme.ttkstyle.configure(
            f'{widget._ttkstyle}.Tab',
            focuscolor='',
            foreground=foreground,
            font=widgetfont,
            padding=(6, 5)
        )
        self.theme.ttkstyle.map(
            f'{widget._ttkstyle}.Tab',
            background=[
                ('selected', colors.background),
                ('!selected', background)
            ],
            lightcolor=[
                ('selected', colors.background),
                ('!selected', background)
            ],
            bordercolor=[
                ('selected', bordercolor),
                ('!selected', bordercolor)
            ],
            padding=[
                ('selected', (6, 5)),
                ('!selected', (6, 5))
            ],
            foreground=[
                ('selected', foreground),
                ('!selected', selectfg)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_panedwindow_assets(self, sashcolor, focuscolor, element, orient):

        sash_size = (40, 5)

        def create_sash(name, x, y, xy, fill):
            img = Image.new('RGBA', (x, y))
            draw = ImageDraw.Draw(img)
            draw.rectangle(xy, fill)
            photoimage = PhotoImage(img)
            self.theme.register_assets({f'{element}.{name}': photoimage})
            return photoimage

        if orient == VERTICAL:
            x, y = sash_size
            normal_xy = [(0, y-2), (x, y-2)]
            active_xy = [(0, y-3), (x, y-1)]
        else:
            y, x = sash_size
            normal_xy = [(x-2, 0), (x-2, y)]
            active_xy = [(x-3, 0), (x-1, y)]

        normal_photoimage = create_sash('normal', x, y, normal_xy, sashcolor)
        active_photoimage = create_sash('active', x, y, active_xy, focuscolor)
        return normal_photoimage, active_photoimage

    def create_panedwindow_style(self, widget):
        # widget colors
        colors = self.theme.colors
        orient = widget._widget_orient

        if self.theme.is_light_theme:
            sashcolor = colors.border
        else:
            sashcolor = colors.selectbg

        focuscolor = colors.get(widget._widget_color) or sashcolor

        # create widget style
        element = uuid4()
        self.theme.ttkstyle.configure(
            widget._ttkstyle, background=colors.background)

        images = self.create_panedwindow_assets(
            sashcolor, focuscolor, element, orient)

        # horizontal sash
        if widget._widget_orient == VERTICAL:
            # 0-normal, 1-active
            self.theme.ttkstyle.element_create(
                f'{element}.sash', 'image', images[0], ('hover', images[1])
            )
            self.theme.ttkstyle.layout(
                f'{widget._ttkstyle}.Horizontal.Sash',
                [(f'{element}.sash', {'sticky': EW})]
            )
            self.theme.register_style(widget._ttkstyle)
        else:
            # 0-normal, 1-active
            self.theme.ttkstyle.element_create(
                f'{element}.sash', 'image', images[0], ('hover', images[1])
            )
            self.theme.ttkstyle.layout(
                f'{widget._ttkstyle}.Vertical.Sash',
                [(f'{element}.sash', {'sticky': NS})]
            )
            self.theme.register_style(widget._ttkstyle)

    def create_progressbar_assets(self, barcolor, troughcolor, bordercolor,
                                  orient, element):
        bar_size = (30, 14)
        x, y = bar_size

        def bar_image(x, y):
            img = Image.new('RGBA', (x, y), barcolor)
            photoimage = PhotoImage(img)
            self.theme.register_assets({f'{element}.bar': photoimage})
            return photoimage

        def trough_image(x, y):
            xy = [0, 0, x-1, y-1] if orient == HORIZONTAL else [x-1, y-1, 0, 0]
            img = Image.new('RGBA', (x, y))
            draw = ImageDraw.Draw(img)
            draw.rectangle(xy, troughcolor, bordercolor, 1)
            photoimage = PhotoImage(img)
            self.theme.register_assets({f'{element}.trough': photoimage})
            return photoimage

        if orient == HORIZONTAL:
            bar_photoimage = bar_image(x, y)
            trough_photoimage = trough_image(x+2, y+2)
        else:
            bar_photoimage = bar_image(y, x)
            trough_photoimage = trough_image(y+2, x+2)

        return bar_photoimage, trough_photoimage

    def create_progressbar_style(self, widget):
        orient = widget._widget_orient

        # widget colors
        colors = self.theme.colors
        barcolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            troughcolor = colors.update_hsv(colors.inputbg, vd=-0.08)
            bordercolor = troughcolor
        else:
            troughcolor = colors.update_hsv(colors.selectbg, vd=-0.08)
            bordercolor = troughcolor

        # build widget style
        element = uuid4()
        bar_image, trough_image = self.create_progressbar_assets(
            barcolor, troughcolor, bordercolor, orient, element)

        if orient == HORIZONTAL:
            self.theme.ttkstyle.element_create(
                f'{element}.pbar', 'image', bar_image, height=14, sticky=EW
            )
            self.theme.ttkstyle.element_create(
                f'{element}.trough', 'image', trough_image, height=16,
                sticky=EW, border=1
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [(f"{element}.trough", {"sticky": NSEW, "children": [
                    (f"{element}.pbar", {"side": LEFT, "sticky": NS})]})]
            )
        else:
            self.theme.ttkstyle.element_create(
                f'{element}.pbar', 'image', bar_image, width=14, sticky=NS
            )
            self.theme.ttkstyle.element_create(
                f'{element}.trough', 'image', trough_image, width=16,
                sticky=NS, border=1
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [(f"{element}.trough", {"sticky": NSEW, "children": [
                    (f"{element}.pbar", {"side": BOTTOM, "sticky": EW})]})]
            )
        self.theme.register_style(widget._ttkstyle)

    def create_striped_progressbar_assets(
            self, barcolor, troughcolor, bordercolor, orient, element):
        # calculate the light bar color
        b = colorsys.rgb_to_hsv(*Colors.hex_to_rgb(barcolor))[2]
        if b < 0.4:
            vd = 0.3
        elif b > 0.9:
            vd = 0
        else:
            vd = 0.1
        lightcolor = Colors.update_hsv(barcolor, sd=-0.2, vd=vd)

        # create image assets
        bar_img = Image.new("RGBA", (100, 100), lightcolor)
        draw = ImageDraw.Draw(bar_img)
        draw.polygon([(0, 0), (48, 0), (100, 52), (100, 100), (100, 100)],
                     fill=barcolor)
        draw.polygon([(0, 52), (48, 100), (0, 100)], fill=barcolor)
        bar_photoimage = PhotoImage(bar_img.resize((14, 14), Image.LANCZOS))
        self.theme.register_assets(
            {f"{element}.{orient[0]}bar": bar_photoimage})

        trough_img = Image.new("RGBA", (16, 16), troughcolor)
        draw = ImageDraw.Draw(trough_img)
        draw.rectangle([0, 0, 15, 15], fill=troughcolor, outline=bordercolor,
                       width=1)
        trough_photoimage = PhotoImage(trough_img)
        self.theme.register_assets({f"{element}.trough": trough_photoimage})

        return bar_photoimage, trough_photoimage

    def create_striped_progressbar_style(self, widget):
        orient = widget._widget_orient

        # widget colors
        colors = self.theme.colors
        barcolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            troughcolor = colors.update_hsv(colors.inputbg, vd=-0.08)
            bordercolor = troughcolor
        else:
            troughcolor = colors.update_hsv(colors.selectbg, vd=-0.08)
            bordercolor = troughcolor

        # build widget style
        element = uuid4()
        bar_image, trough_image = self.create_striped_progressbar_assets(
            barcolor, troughcolor, bordercolor, orient, element)

        if orient == HORIZONTAL:
            self.theme.ttkstyle.element_create(
                f'{element}.pbar', 'image', bar_image, height=14, sticky=EW
            )
            self.theme.ttkstyle.element_create(
                f'{element}.trough', 'image', trough_image, height=16,
                sticky=EW, border=1
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [(f"{element}.trough", {"sticky": NSEW, "children": [
                    (f"{element}.pbar", {"side": LEFT, "sticky": NS})]})]
            )
        else:
            self.theme.ttkstyle.element_create(
                f'{element}.pbar', 'image', bar_image, width=14, sticky=NS
            )
            self.theme.ttkstyle.element_create(
                f'{element}.trough', 'image', trough_image, width=16,
                sticky=NS, border=1
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [(f"{element}.trough", {"sticky": NSEW, "children": [
                    (f"{element}.pbar", {"side": BOTTOM, "sticky": EW})]})]
            )
        self.theme.register_style(widget._ttkstyle)

    def create_radiobutton_assets(self, indicatorcolor, element):

        indicator_size = (134, 134)
        offset = 3

        def button_image(name, fill, outline, dot='white'):
            x, y = indicator_size
            img = Image.new('RGBA', (indicator_size))
            draw = ImageDraw.Draw(img)
            draw.ellipse(
                xy=[offset, offset, x-offset, y-offset],
                outline=outline,
                width=3,
                fill=fill
            )
            if name == 'on':
                draw.ellipse([40, 40, 94, 94], fill=dot)
            photoimage = PhotoImage(img.resize((14, 14), Image.LANCZOS))
            self.theme.register_assets({f'{element}.{name}': photoimage})
            return photoimage

        # style colors
        colors = self.theme.colors
        outline = colors.selectbg

        if self.theme.is_light_theme:
            fill = colors.inputbg
            offcolor = fill
            disabledfg = colors.update_hsv(colors.inputbg, vd=-0.2)
            disabledbg = colors.inputbg
        else:
            fill = colors.foreground
            offcolor = outline
            disabledfg = Colors.update_hsv(colors.inputbg, vd=-0.3)
            disabledbg = colors.selectbg

        # create image assets
        off_photoimage = button_image('off', offcolor, outline)
        on_photoimage = button_image(
            'on', indicatorcolor, indicatorcolor, fill)
        disabled_photoimage = button_image('disabled', disabledbg, disabledfg)

        return off_photoimage, on_photoimage, disabled_photoimage

    def create_radiobutton_style(self, widget):
        widgetfont = 'TkDefaultFont'

        # style colors
        colors = self.theme.colors
        background = colors.background
        foreground = colors.foreground
        indicatorcolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            disabled = colors.border
        else:
            disabled = colors.selectbg

        # create image assets
        element = uuid4()
        radio_off, radio_on, radio_disabled =\
            self.create_radiobutton_assets(indicatorcolor, element)

        # build widget style
        self.theme.ttkstyle.element_create(
            f'{element}.Radiobutton.indicator', 'image', radio_on,
            ('disabled', radio_disabled),
            ('!selected', radio_off),
            width=20, border=4, sticky=W
        )
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            background=background,
            foreground=foreground,
            focuscolor='',
            font=widgetfont,
            padding=2
        )
        self.theme.ttkstyle.layout(
            widget._ttkstyle,
            [("Radiobutton.padding", {"children": [
                (f"{element}.Radiobutton.indicator",
                 {"side": LEFT, "sticky": ""}),
                ("Radiobutton.focus", {"children": [
                    ("Radiobutton.label", {"sticky": NSEW})],
                    "side": LEFT, "sticky": "", })],
                "sticky": NSEW})]
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            foreground=[
                ('disabled', disabled),
                ('active', indicatorcolor)
            ]
        )
        self.theme.register_style(widget._ttkstyle)

    def create_scale_assets(self, handlecolor, troughcolor, disabled, orient,
                            element):

        handle_size = (150, 150)
        trough_size = (280, 130)

        def handle_image(name, size, fill):
            x, y = size
            img = Image.new('RGBA', size)
            draw = ImageDraw.Draw(img)
            draw.ellipse((2, 2, x-2, y-2), fill=fill)
            photoimage = PhotoImage(img.resize((x//10, y//10), Image.CUBIC))
            self.theme.register_assets({f'{element}.{name}': photoimage})
            return photoimage

        def trough_image(name, size):
            x, y = size
            img = Image.new('RGBA', size)
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle(
                xy=(40, 40, x-40, y-40),
                radius=y//2,
                fill=troughcolor,
                outline=outline,
                width=5
            )
            photoimage = PhotoImage(img.resize((x//10, y//10), Image.CUBIC))
            self.theme.register_assets({f'{element}.{name}': photoimage})
            return photoimage

        # style colors
        colors = self.theme.colors
        outline = troughcolor

        if self.theme.is_light_theme:
            pressed = colors.update_hsv(handlecolor, vd=-0.2)
            hover = colors.update_hsv(handlecolor, vd=-0.1)
        else:
            pressed = colors.update_hsv(handlecolor, vd=0.35)
            hover = colors.update_hsv(handlecolor, vd=0.25)

        # create widget style assets
        normal_photoimage = handle_image('normal', handle_size, handlecolor)
        pressed_photoimage = handle_image('pressed', handle_size, pressed)
        disabled_photoimage = handle_image('disabled', handle_size, disabled)
        hover_photoimage = handle_image('hover', handle_size, hover)

        if orient == HORIZONTAL:
            trough_photoimage = trough_image('trough', trough_size)
        else:
            trough_photoimage = trough_image('trough', trough_size[::-1])

        return (normal_photoimage, pressed_photoimage, disabled_photoimage,
                hover_photoimage, trough_photoimage)

    def create_scale_style(self, widget):
        orient = widget._widget_orient

        # style colors
        colors = self.theme.colors
        background = colors.background
        handlecolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            troughcolor = colors.update_hsv(colors.inputbg, vd=-0.1)
            disabled = colors.update_hsv(colors.inputbg, vd=-0.2)
        else:
            troughcolor = colors.update_hsv(colors.selectbg, vd=-0.1)
            disabled = colors.update_hsv(colors.inputbg, vd=-0.3)

        # create style assets
        element = uuid4()
        # 0-normal, 1-pressed, 2-disabled, 3-hover, 4-trough
        images = self.create_scale_assets(handlecolor, troughcolor, disabled,
                                          orient, element)

        if orient == HORIZONTAL:
            self.theme.ttkstyle.element_create(
                f'{element}.track', 'image', images[4], border=6, height=13
            )
            self.theme.ttkstyle.element_create(
                f'{element}.slider', 'image', images[0],
                ('disabled', images[2]),
                ('pressed', images[1]),
                ('hover', images[3]),
                height=15, width=15
            )
            self.theme.ttkstyle.configure(

                widget._ttkstyle,
                background=background
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [("Scale.focus", {"expand": YES, "sticky": NSEW, "children": [
                    (f"{element}.track", {"sticky": EW}),
                    (f"{element}.slider", {"side": LEFT, "sticky": ""})]})]
            )
        else:
            self.theme.ttkstyle.element_create(
                f'{element}.track', 'image', images[4], border=6, width=13
            )
            self.theme.ttkstyle.element_create(
                f'{element}.slider', 'image', images[0],
                ('disabled', images[2]),
                ('pressed', images[1]),
                ('hover', images[3]),
                height=15, width=15
            )
            self.theme.ttkstyle.configure(
                widget._ttkstyle,
                background=background
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [("Scale.focus", {"expand": YES, "sticky": NSEW, "children": [
                    (f"{element}.track", {"sticky": NS}),
                    (f"{element}.slider", {"side": TOP, "sticky": ""})]})]
            )
        self.theme.register_style(widget._ttkstyle)

    def create_scrollbar_assets(self, thumbcolor, troughcolor, bordercolor,
                                orient, element, thickness):

        def rounded_rect(name, x, y, fill):
            img = Image.new('RGBA', (x, y))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((1, 1, x-1, y-1), min([x, y]) // 2, fill)
            photoimage = PhotoImage(img.resize((x//10, y//10), Image.CUBIC))
            self.theme.register_assets({f'{element}.{name}': photoimage})
            return photoimage

        def regular_rect(name, x, y, fill, outline):
            img = Image.new('RGBA', (x, y))
            draw = ImageDraw.Draw(img)
            draw.rectangle((0, 0, x-1, y-1), fill, outline, 1)
            photoimage = PhotoImage(img)
            self.theme.register_assets({f'{element}.{name}': photoimage})
            return photoimage

        if self.theme.is_light_theme:
            pressed = Colors.update_hsv(thumbcolor, vd=-0.35)
            active = Colors.update_hsv(thumbcolor, vd=-0.25)
        else:
            pressed = Colors.update_hsv(thumbcolor, vd=0.35)
            active = Colors.update_hsv(thumbcolor, vd=0.25)

        x = thickness * 10
        y = int(thickness * 3.5 * 10)

        if orient == VERTICAL:
            normal_img = rounded_rect('normal', x, y, thumbcolor)
            pressed_img = rounded_rect('pressed', x, y, pressed)
            active_img = rounded_rect('active', x, y, active)
            trough_img = regular_rect(
                'trough', x//10+2, y//10+2, troughcolor, bordercolor)

        else:
            normal_img = rounded_rect('normal', y, x, thumbcolor)
            pressed_img = rounded_rect('pressed', y, x, pressed)
            active_img = rounded_rect('active', y, x, active)
            trough_img = regular_rect('trough', y, x, troughcolor, bordercolor)

        return normal_img, pressed_img, active_img, trough_img

    def create_scrollbar_style(self, widget, thickness):
        orient = widget._widget_orient

        # style colors
        colors = self.theme.colors
        troughcolor = colors.update_hsv(colors.background, vd=0.2)
        bordercolor = troughcolor

        if self.theme.is_dark_theme:
            thumbcolor = (
                colors.get(widget._widget_color) or
                colors.update_hsv(colors.selectbg, vd=0.35, sd=-0.1)
            )
        else:
            thumbcolor = (
                colors.get(widget._widget_color) or
                colors.update_hsv(colors.background, vd=-0.25)
            )

        # create widget assets
        element = uuid4()
        images = self.create_scrollbar_assets(
            thumbcolor, troughcolor, bordercolor, orient, element, thickness)

        layout_borders = [(thickness, 0), (0, thickness)]

        if orient == HORIZONTAL:
            # 0-normal, 1-pressed, 2-active, 3-trough
            self.theme.ttkstyle.element_create(
                f'{element}.thumb', 'image', images[0],
                ('pressed', images[1]), ('active', images[2]),
                border=layout_borders[0], sticky=EW, height=thickness
            )
            self.theme.ttkstyle.element_create(
                f'{element}.trough', 'image', images[3],
                border=layout_borders[0], padding=0, height=thickness+2
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [(f"{element}.trough", {"sticky": EW, "children": [
                    (f"{element}.thumb", {"expand": YES, "sticky": EW})]})]
            )
        else:
            # 0-normal, 1-pressed, 2-active, 3-trough
            self.theme.ttkstyle.element_create(
                f'{element}.thumb', 'image', images[0],
                ('pressed', images[1]), ('active', images[2]),
                border=layout_borders[1], sticky=NS, width=thickness
            )
            self.theme.ttkstyle.element_create(
                f'{element}.trough', 'image', images[3],
                border=layout_borders[1], padding=0, width=thickness+2
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [(f"{element}.trough", {"sticky": NS, "children": [
                    (f"{element}.thumb", {"expand": YES, "sticky": NS})]})]
            )
        self.theme.register_style(widget._ttkstyle)

    def create_separator_style(self, widget):

        # style settings
        orient = widget._widget_orient
        sash_thickness = 1

        # widget colors
        colors = self.theme.colors

        if self.theme.is_light_theme:
            sashcolor = colors.get(widget._widget_color) or colors.border
        else:
            sashcolor = colors.get(widget._widget_color) or colors.selectbg

        # widget assets
        element = uuid4()
        h_photoimage = PhotoImage(
            Image.new("RGB", (40, sash_thickness), sashcolor))
        v_photoimage = PhotoImage(
            Image.new("RGB", (sash_thickness, 40), sashcolor))

        self.theme.register_assets({
            f"{element}.h.separator": h_photoimage,
            f"{element}.v.separator": v_photoimage}
        )

        # build widget style
        if orient == HORIZONTAL:
            self.theme.ttkstyle.element_create(
                f'{element}.Horizontal.Separator.separator', 'image', h_photoimage
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [(f"{element}.Horizontal.Separator.separator", {"sticky": EW})]
            )
        else:
            self.theme.ttkstyle.element_create(
                f'{element}.Vertical.Separator.separator', 'image', v_photoimage
            )
            self.theme.ttkstyle.layout(
                widget._ttkstyle,
                [(f"{element}.Vertical.Separator.separator", {"sticky": NS})]
            )
        self.theme.register_style(widget._ttkstyle)

    def create_sizegrip_assets(self, gripcolor, element):
        image = Image.new('RGBA', (14, 14))
        draw = ImageDraw.Draw(image)

        # top row
        draw.rectangle((9, 3, 10, 4), fill=gripcolor)

        # middle row
        draw.rectangle((6, 6, 7, 7), fill=gripcolor)  # middle row
        draw.rectangle((9, 6, 10, 7), fill=gripcolor)

        # bottom row
        draw.rectangle((3, 9, 4, 10), fill=gripcolor)  # bottom row
        draw.rectangle((6, 9, 7, 10), fill=gripcolor)
        draw.rectangle((9, 9, 10, 10), fill=gripcolor)

        grip_photoimage = PhotoImage(image)
        self.theme.register_assets({f"{element}.sizegrip": grip_photoimage})
        return grip_photoimage

    def create_sizegrip_style(self, widget):
        # widget colors
        colors = self.theme.colors
        background = colors.background

        if self.theme.is_light_theme:
            gripcolor = colors.get(widget._widget_color) or colors.border
        else:
            gripcolor = colors.get(widget._widget_color) or colors.inputbg

        # create style assets
        element = uuid4()
        grip_photoimage = self.create_sizegrip_assets(gripcolor, element)

        # create widget style
        self.theme.ttkstyle.configure(widget._ttkstyle, background=background)
        self.theme.ttkstyle.layout(
            widget._ttkstyle,
            [(f"{element}.Sizegrip.sizegrip", {"side": BOTTOM, "sticky": SE})]
        )
        self.theme.ttkstyle.element_create(
            f'{element}.Sizegrip.sizegrip', 'image', grip_photoimage
        )
        self.theme.register_style(widget._ttkstyle)

    def create_spinbox_style(self, widget):
        # widget colors
        colors = self.theme.colors
        background = colors.inputbg
        foreground = colors.inputfg
        focuscolor = colors.get(widget._widget_color) or colors.primary

        if self.theme.is_light_theme:
            disabledfg = colors.update_hsv(foreground, vd=-0.2)
            bordercolor = colors.border
        else:
            disabledfg = colors.update_hsv(foreground, vd=-0.3)
            bordercolor = colors.selectbg

        # create widget style
        element = uuid4()
        self.theme.ttkstyle.element_create(
            f'{element}.Spinbox.uparrow', 'from', 'default'
        )
        self.theme.ttkstyle.element_create(
            f'{element}.Spinbox.downarrow', 'from', 'default'
        )
        self.theme.ttkstyle.layout(
            widget._ttkstyle,
            [(f"{element}.Spinbox.field", {"side": TOP, "sticky": EW, "children": [
                ("null", {"side": RIGHT, "sticky": "", "children": [
                    (f"{element}.Spinbox.uparrow", {"side": TOP, "sticky": E}),
                    (f"{element}.Spinbox.downarrow",
                     {"side": BOTTOM, "sticky": E}),
                ]}),
                ("Spinbox.padding", {"sticky": NSEW, "children": [
                    ("Spinbox.textarea", {"sticky": NSEW})]})]})]
        )

        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            arrowsize=12,
            arrowcolor=foreground,
            bordercolor=bordercolor,
            darkcolor=background,
            lightcolor=background,
            foreground=foreground,
            font='TkTextFont',
            fieldbackground=background,
            insertcolor=foreground,
            background=background,
            selectbackground=colors.selectbg,
            relief=FLAT,
            padding=5
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            arrowcolor=[
                ('disabled', disabledfg),
                ('pressed', focuscolor),
                ('focus', focuscolor),
                ('hover', focuscolor)
            ],
            bordercolor=[
                ('focus !disabled', focuscolor),
                ('hover !disabled', focuscolor)
            ],
            foreground=[('disabled', disabledfg)],
            # darkcolor=[
            #     ('focus !disabled', focuscolor),
            #     ('hover !disabled', background)
            # ],
            # lightcolor=[
            #     ('focus !disabled', focuscolor),
            #     ('hover !disabled', background)
            # ]
        )
        self.theme.register_style(widget._ttkstyle)

    def update_text_style(self, widget):
        colors = self.theme.colors
        
        widget.configure(
            background=colors.inputbg,
            foreground=colors.inputfg,
            insertbackground=colors.inputfg,
            selectbackground=colors.selectbg,
            selectforeground=colors.selectfg,
            relief=FLAT,
            borderwidth=0,
            highlightthickness=0,
            insertwidth=1,
            font='TkTextFont'
        )
        frame_style = ''.join(widget._bootstyle)
        if widget.focusframe:
            frame_style += FOCUSFRAME
            widget.container._bootstyle = frame_style
            widget.container._configure_bootstyle(self)

    def create_treeview_style(self, widget):

        row_height = 20
        header_padding = 0
        header_font = 'TkHeadingFont'
        input_font = 'TkTextFont'

        # widget colors
        colors = self.theme.colors

        if not widget._widget_color:
            headerbg = colors.inputbg
            headerfg = colors.inputfg
            focuscolor = colors.primary
        else:
            headerbg = colors.get(widget._widget_color)
            headerfg = colors.selectfg
            focuscolor = headerfg

        if self.theme.is_light_theme:
            disabledfg = colors.update_hsv(colors.inputfg, vd=-0.2)
            bordercolor = colors.border
        else:
            disabledfg = colors.update_hsv(colors.inputfg, vd=-0.2)
            bordercolor = colors.selectbg

        # create widget style
        element = uuid4()
        self.theme.ttkstyle.element_create(
            f'{element}.Treeitem.indicator', 'from', 'alt'
        )
        self.theme.ttkstyle.layout(
            f'{widget._ttkstyle}.Item',
            [("Treeitem.padding", {"sticky": "nswe", "children": [
                (f"{element}.Treeitem.indicator",
                 {"side": "left", "sticky": ""}),
                ("Treeitem.image", {"side": "left", "sticky": ""}),
                ("Treeitem.focus", {"side": "left", "sticky": "", "children": [
                    ("Treeitem.text", {"side": "left", "sticky": ""})]})]})]
        )
        self.theme.ttkstyle.configure(
            widget._ttkstyle,
            background=colors.inputbg,
            foreground=colors.inputfg,
            fieldbackground=colors.inputbg,
            font=input_font,
            borderwidth=2,
            padding=0,
            bordercolor=bordercolor,
            lightcolor=colors.inputbg,
            rowheight=row_height
        )
        self.theme.ttkstyle.map(
            widget._ttkstyle,
            background=[('selected', colors.selectbg)],
            # lightcolor=[('focus', focuscolor)],
            foreground=[
                ('disabled', disabledfg),
                ('selected', colors.selectfg)
            ],
            bordercolor=[
                ('focus', focuscolor),
                ('hover', focuscolor)
            ]
        )
        # for some reason, I can't configure more than one
        #   header option at a time... something is messed up.
        heading_style = f'{widget._ttkstyle}.Heading'
        self.theme.ttkstyle.configure(heading_style, background=headerbg)
        self.theme.ttkstyle.configure(heading_style, foreground=headerfg)
        self.theme.ttkstyle.configure(heading_style, padding=header_padding)
        self.theme.ttkstyle.configure(heading_style, font=header_font)
        self.theme.register_style(widget._ttkstyle)

    def update_window_style(self, widget):
        # update default styles
        colors = self.theme.colors
        self.theme.ttkstyle.configure('.',
                                      background=colors.background,
                                      darkcolor=colors.border,
                                      foreground=colors.foreground,
                                      troughcolor=colors.background,
                                      selectbg=colors.selectbg,
                                      selectfg=colors.selectfg,
                                      selectforeground=colors.selectfg,
                                      selectbackground=colors.selectbg,
                                      fieldbg='white',
                                      borderwidth=1,
                                      focuscolor=''
                                      )
        header_font = tkFont.nametofont('TkHeadingFont')
        header_font.configure(weight='bold')
        # update window style
        background = colors.get(widget._widget_color) or colors.background
        widget.configure(background=background)
