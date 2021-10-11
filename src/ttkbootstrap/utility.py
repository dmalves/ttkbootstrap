import re

WIDGET_LOOKUP = {
    "button": "TButton",
    "btn": "TButton",
    "progressbar": "TProgressbar",
    "progress": "TProgressbar",
    "check": "TCheckbutton",
    "checkbutton": "TCheckbutton",
    "checkbtn": "TCheckbutton",
    "combo": "TCombobox",
    "combobox": "TCombobox",
    "frame": "TFrame",
    "inputframe": "Input.TFrame",
    "floodgauge": "TFloodgauge",
    "gauge": "TFloodgauge",
    "grip": "TSizegrip",
    "lbl": "TLabel",
    "label": "TLabel",
    "labelframe": "TLabelframe",
    "lblframe": "TLabelframe",
    "lblfrm": "TLabelframe",
    "radio": "TRadiobutton",
    "radiobutton": "TRadiobutton",
    "radiobtn": "TRadiobutton",
    "roundtoggle": "Roundtoggle.Toolbutton",
    "separator": "TSeparator",
    "scrollbar": "TScrollbar",
    "sizegrip": "TSizegrip",
    "scale": "TScale",
    "slider": "TScale",
    "squaredtoggle": "Toggle.Toolbutton",
    "toggle": "Toggle.Toolbutton",
    "roundedtoggle": "Toggle.Toolbutton",
    "toolbutton": "Toolbutton",
    "tool": "Toolbutton",
    "tree": "Treeview",
    "treeview": "Treeview",
}

WIDGET_PATTERN = "|".join(WIDGET_LOOKUP.keys())
COLOR_PATTERN = re.compile(r"primary|secondary|success|info|warning|danger")
ORIENT_PATTERN = re.compile(r"horizontal|vertical")
STYLE_PATTERN = re.compile(
    r"outline|link|inverse|rounded|striped|squared|focusframe"
)


def normalize_style(bootstyle):
    """Remove all spaces and capitalization in the style keywords and
    return the resulting string

    Parameters
    ----------
    bootstyle : Union[str, Iterable]
        A string of widget style keywords.

    Returns
    -------
    str
        A string with all spaces and capitalization removed.

    """
    if bootstyle:
        return "".join(bootstyle).lower()
    else:
        return ""


def find_widget_color(bootstyle):
    """Extract and return the style color from the style keywords.

    The matching color is based on a regex pattern match from color
    patterns in the COLOR_PATTERN constant.

    Parameters
    ----------
    bootstyle : str
        A string of widget style keywords.

    Returns
    -------
    str
        A matching style color.
    """
    match = re.search(COLOR_PATTERN, bootstyle)
    return "" if not match else match.group(0)


def find_bootstyle_orient(widget_class, orient):
    """Extract, modify, and return the widget style orientation.

    Returns a lowercased orientation appended with a "." if an
    orientation is present. This is required to build the style name
    provided to ttk. Otherwise, an empty string is returned.
    """
    if not orient:
        if widget_class in ["TProgressbar", "TScale", "TSeparator"]:
            return "Horizontal."
        elif widget_class in ["TPanedwindow", "TScrollbar"]:
            return "Vertical."
        else:
            return ""
    else:
        return orient.lower().title() + "."


def find_bootstyle_type(freestyle):
    """Extract and return the style type from the style keywords.

    The matching style is based on a regex pattern match from style
    types in the STYLE_PATTERN constant. If found, a "." is appended to
    the end so that a ttk style can be built. Otherwise, an empty
    string is returned.

    Parameters
    ----------
    style : str
        A string of widget style keywords.

    Returns
    -------
    str
        A matching style style.

    """
    match = re.search(STYLE_PATTERN, freestyle)
    return "" if not match else match.group(0).title() + "."


def find_bootstyle_widget_class(bootstyle, widget_class) -> str:
    """Extract and return the widget class.

    The matching style is based on a regex pattern match from widget
    types in the WIDGET_PATTERN constant. If not found, then the
    fallback widget_class is returned.

    The reason for this distinction is because it is possible to style
    one type of widget with the style of another... for example, one
    can use a TButton style on a TLabel widget and inherit the hover
    effects, etc... from the button on the label. So, the expected
    style widget class must be evaluated before falling back to the
    actual widget_class of the widget.

    Parameters
    ----------
    bootstyle : str
        A string of widget style keywords.

    widget_class : str
        The class of the widget. ie. as returned by the winfo_class
        method for tk and ttk widgets.

    Returns
    -------
    str
        The matching widget_class pattern or the fallback widget
        class.
    """
    match = re.search(WIDGET_PATTERN, bootstyle)
    return widget_class if not match else WIDGET_LOOKUP.get(match.group(0))


def create_ttk_style(widget):
    """Parse the raw style keywords and build a real ttk style name
    that will be used when building the widget style. These style
    keywords trigger different settings and procedures in the
    theme_builder.
    """
    color = "" if not widget._widget_color else widget._widget_color + "."
    w_type = find_bootstyle_type(widget._bootstyle)
    orient = find_bootstyle_orient(widget._widget_class, widget._widget_orient)
    w_class = find_bootstyle_widget_class(
        widget._bootstyle, widget._widget_class)
    widget._ttkstyle = f"{color}{w_type}{orient}{w_class}"
