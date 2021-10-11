from tkinter import ttk
from typing import Any, List
from ttkbootstrap.theme.theme import ThemeBuilder
from ttkbootstrap.widgets.widget import Widget
from ttkbootstrap import utility
from ttkbootstrap.constants import *


class Listbox(Widget, ttk.Treeview):
    def __init__(self, master=None, bootstyle='primary', values=[],
                 width=200, anchor=W, **kwargs):
        Widget.__init__(self, bootstyle, 'TListbox.Treeview')

        # add arguments to transform treeview into listbox
        kwargs.update(
            show='',
            columns=1,
            selectmode=kwargs.get('selectmode') or BROWSE,
            takefocus=True
        )
        ttk.Treeview.__init__(self, master=master, **kwargs)

        # column configure
        ttk.Treeview.column(self,
                            1,
                            width=width,
                            anchor=anchor,
                            minwidth=20,
                            stretch=True
                            )

        # add initial values
        for row in values:
            ttk.Treeview.insert(self, '', 'end', values=row)

        # Theme change will trigger rebuild of styles (if needed)
        self.bind('<<ThemeChanged>>', self._configure_bootstyle)

        # exclude incompatible treeview methods; this does not prevent
        #   them from being show in intellisense, but they will raise
        #   an `AttributeError` when called, and will not show up when
        #   using the `dir` method.
        self.__excluded_methods = set([
            'column', 'detach', 'exists', 'focus', 'heading',
            'identify', 'instate', 'item', 'move', 'columnconfigure',
            'next', 'parent', 'prev', 'set', 'selection_toggle'])
        self.__exclude_treeview_methods()

    def __exclude_treeview_methods(self):
        for m in self.__excluded_methods:
            def raise_error(*args, **kwargs):
                # treeview methods not compatible with listobx
                raise AttributeError(
                    "Treeview method not compatible with Listbox")
            setattr(self, m, raise_error)

    def __dir__(self):
        attributes = set(dir(ttk.Treeview)) | set(
            dir(Widget)) | set(dir(super()))
        return sorted(attributes - self.__excluded_methods)

    def _configure_bootstyle(self, *args):
        self._bootstyle = utility.normalize_style(self._bootstyle)
        self._widget_color = utility.find_widget_color(self._bootstyle)

        # create ttk style from bootstyle keywords
        utility.create_ttk_style(self)

        #  build actual ttk style if not already existing
        builder: ThemeBuilder = self._theme.theme_builder

        if not self._theme.style_exists(self._ttkstyle):
            builder.create_listbox_style(self)

        # set the widget ttk style
        self.configure(style=self._ttkstyle)

    def _get_children(self):
        return ttk.Treeview.get_children(self)

    def activate(self, index: int):
        """Sets the active element to the one indicated by `index`. If
        `index` is outside the range of elements in the listbox, the
        closest element is activated."""
        children = self._get_children()
        try:
            ttk.Treeview.selection_set(self, children[index])
        except:
            ttk.Treeview.selection_set(self, children[-1])

    def index(self, index: Any) -> Any:
        """Returns the integer index value that corresponds to index.
        If index is *end*, then return value is a count of the number
        of elements in the listbox, (not the index of the last time).

        Parameters
        ----------
        index : { int, 'active', 'first', 'last', 'end', '@y' }
            The numeric index of `index`.

        Returns
        -------
        int
            The integer index of `index`.
        """
        children = self._get_children()
        try:
            if index == 'first':
                return 0
            elif index == 'last':
                return len(children) - 1
            elif index == 'end':
                return len(children)
            elif index == 'active':
                itemid = ttk.Treeview.focus(self)
                return children.index(itemid)
            elif '@' in str(index):
                _, i = index.split('@')
                if i:
                    itemid = ttk.Treeview.identify_row(self, i)
                    return children.index(itemid)
                else:
                    return
            else:
                i = int(index)
                return i
        except:
            return

    def curselection(self) -> List[int]:
        """Returns a list containing the numerical indices of all 
        elements in the listbox that are currently selected."""
        children = ttk.Treeview.get_children(self, '')
        selected = ttk.Treeview.selection(self)
        return [children.index(s) for s in selected]

    def delete(self, first, last=None):
        """Deletes one or more elements in the listbox. `first` and 
        `last` are indices specifying the first and last elements in 
        the range to delete. If `last` is not specified, it defaults 
        to `first` and a single element will be deleted.

        Parameters
        ----------
        first : int
            The first element in the range to delete.

        last : int, optional
            The last element in the range to delete.
        """
        children = self._get_children()
        first_index = self.index(first)
        last_index = self.index(last)
        if last is None:
            ttk.Treeview.delete(self, children[first_index])
        else:
            ttk.Treeview.delete(self, *children[first_index:last_index+1])

    def get(self, first, last=None):
        """Returns the contents of the listbox elements indicated by
        the indices in the range from first to last. If last is None,
        a single element will be return at index `first`.

        Parameters
        ----------
        first : Any
            The first element in the range.

        last : Any, optional
            The last element in the range (inclusive)

        Returns
        -------
        Union[Any, List[Any]]
            The contents of the listbox in the range specified.
        """
        first_index = self.index(first)
        last_index = self.index(last)

        children = self._get_children()
        if last is None and first_index < len(children):
            itemid = children[first_index]
            value = ttk.Treeview.item(self, itemid, 'values')[0]
            return value
        elif first_index >= 0 and last_index <= len(children):
            values = []
            for i in range(first_index, last_index+1):
                value = ttk.Treeview.item(self, children[i], 'values')[0]
                values.append(value)
            return values

    def insert(self, index, *elements):
        """Inserts zero or more new elements in the list just before
        the element given by `index`. If `index` if specified as `end`
        then the new elements are added to the end of the list.

        Index can take one of the following forms:
            { int, 'active', 'first', 'last', 'end', '@y' }

        Parameters
        ----------
        index : Any
            The starting index from which to insert.

        *elements : Any
            The values to insert into the list.
        """
        insert_index = self.index(index)
        for item in elements:
            ttk.Treeview.insert(self, '', insert_index, values=[item])
            insert_index += 1

    def itemcget(self, index, option):
        """Retruns the value of the item configuration option given by
        `option`. Options may have any of the values accepted by the
        `itemconfigure` method.

        Parameters
        ----------
        index : Any
            The index of the lookup item

        option : { value, tags }

        Returns
        -------
        Any
            The value of option for index
        """
        configuration = self.itemconfigure(index)
        if option == 'value':
            value = configuration.get('value')
            if len(value) > 0:
                return value[0]
            else:
                return value
        else:
            return configuration.get(option)

    def itemconfigure(self, index, option=None, **kw):
        """If no options are given, a dict with options/values for the 
        item is returned. If option is specified then the value for 
        that option is returned. Otherwise, sets the options to the 
        corresponding values as given by kw.
        """
        # TODO strip out the text, image, and open options
        item_index = self.index(index)
        children = self._get_children()
        try:
            itemid = children[item_index]
        except IndexError:
            return
        return ttk.Treeview.item(self, itemid, option, **kw)

    def nearest(self, y: int):
        """Given a y-coordinate with the listbox window, this command 
        returns the visible index of the of the listbox element nearest
        that of the y-coordinate."""
        return self.index(f'@{y}')

    def scan(self):
        raise NotImplementedError

    def see(self, index: int):
        """Adjust the view in the listbox so that the element given by
        `index` is visible.

        Index can take one of the following forms:
            { int, 'active', 'first', 'last', 'end', '@y' }
        """
        children = self._get_children()
        try:
            itemid = children[index]
        except:
            return
        ttk.Treeview.see(self, itemid)

    def selection(self):
        """Returns list of selected items. Alias for `curselection`"""
        return self.curselection()

    def selection_set(self, *indices):
        """Add all of the specified by the indices to the selection.

        An index can take one of the following forms:
            { int, 'active', 'first', 'last', 'end', '@y' }
        """
        items_to_add = []
        for i in indices:
            items_to_add.append(self.index(i))
        ttk.Treeview.selection_add(self, *items_to_add)

    def selection_clear(self, first, last):
        """Clear the selection for any element between `first` and
        `last`. 

        Index can take one of the following forms:
            { int, 'active', 'first', 'last', 'end', '@y' }

        Parameters
        ----------
        first : Any
            The first element in the range.

        last : Any
            The last element in the range.
        """
        selected = self.curselection()
        children = self._get_children()
        first_index = self.index(first)
        last_index = self.index(last)
        toggle_list = []
        for index in range(first_index, last_index):
            if index in selected:
                toggle_list.append(children[index])
        ttk.Treeview.selection_toggle(self, toggle_list)

    def selection_includes(self, index: Any):
        """Returns `True` if the element indicated by `index` is 
        currently selected, False if it is not.

        Index can take one of the following forms:
            { int, 'active', 'first', 'last', 'end', '@y' }

        Parameters
        ----------
        index : Any
            The index to check.
        """
        select_index = self.index(index)
        selected = self.curselection()
        return select_index in selected

    def size(self):
        children = self._get_children()
        return len(children)
