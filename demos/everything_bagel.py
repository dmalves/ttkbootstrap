import ttkbootstrap as ttk

ZEN = """Beautiful is better than ugly. 
Explicit is better than implicit. 
Simple is better than complex. 
Complex is better than complicated.
Flat is better than nested. 
Sparse is better than dense.  
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""


app = ttk.Window('ttkbootstrap Widget Demo', 'superhero')

# horizontal scrollbar
sb1 = ttk.Scrollbar(app, orient=ttk.HORIZONTAL)
sb1.pack(side=ttk.BOTTOM, fill=ttk.X, expand=ttk.YES, padx=10, pady=10)
sb1.set(0.2, 0.6)

# horizontal progressbar
pb = ttk.Progressbar(app, value=75, bootstyle=ttk.STRIPED)
pb.pack(side=ttk.BOTTOM, fill=ttk.X, expand=ttk.YES, padx=10)
pb.start(100)

lframe = ttk.Frame(app, padding=10)
lframe.pack(side=ttk.LEFT, fill=ttk.BOTH)
rframe = ttk.Frame(app, padding=10)
rframe.pack(side=ttk.RIGHT, fill=ttk.BOTH)

# ---------- SECTION 1 -------------------------------------------------

theme_frame = ttk.Frame(lframe)
theme_frame.pack(fill=ttk.X, pady=15, side=ttk.TOP)

# The change combo & label
ttk.Label(theme_frame, text="Theme").pack(side=ttk.LEFT)

cbo = ttk.Combobox(theme_frame, text=app.theme.name, values=app.theme.theme_names(),
                   bootstyle=ttk.INFO)
cbo.pack(side=ttk.LEFT, padx=10)
cbo.current(0)


def change_theme(e):
    t = cbo.get()
    app.theme.use(t)
    app.configure(background=app.theme.colors.background)


cbo.bind_select_command(change_theme)

cb1 = ttk.Checkbutton(theme_frame, text="rounded toggle",
                      bootstyle=(ttk.ROUNDED, ttk.TOGGLE, ttk.SUCCESS), selected=True)
cb1.pack(side=ttk.RIGHT)

cb2 = ttk.Checkbutton(theme_frame, text="squared toggle",
                      bootstyle=(ttk.SQUARED, ttk.TOGGLE), selected=True)
cb2.pack(side=ttk.RIGHT, padx=10)

# shared settings for pack configuration
cnf = {'side': ttk.LEFT, 'expand': ttk.YES, 'padx': 5}

# checkbutton group
cb_group = ttk.Labelframe(lframe, text="Check & Toggle buttons", padding=10)
cb_group.pack(fill=ttk.X, side=ttk.TOP)

ttk.Checkbutton(cb_group, text="primary", selected=True).pack(**cnf)
ttk.Checkbutton(cb_group, text="secondary", selected=True,
                bootstyle=ttk.SECONDARY).pack(**cnf)
ttk.Checkbutton(cb_group, text="success", selected=True,
                bootstyle=ttk.SUCCESS).pack(**cnf)
ttk.Checkbutton(cb_group, text="info", selected=True,
                bootstyle=ttk.INFO).pack(**cnf)
ttk.Checkbutton(cb_group, text="warning", selected=True,
                bootstyle=ttk.WARNING).pack(**cnf)
ttk.Checkbutton(cb_group, text="danger", selected=True,
                bootstyle=ttk.DANGER).pack(**cnf)
ttk.Checkbutton(cb_group, text="disabled", selected=True,
                state=ttk.DISABLED).pack(**cnf)

# # radio button group
radio_var = ttk.Variable()
rb_group = ttk.Labelframe(lframe, text="Radiobuttons", padding=10)
rb_group.pack(fill=ttk.X, pady=10, side=ttk.TOP)
ttk.Radiobutton(rb_group, value=1, text="primary", variable=radio_var,
                selected=True).pack(**cnf)
ttk.Radiobutton(rb_group, value=2, text="secondary", variable=radio_var,
                bootstyle=ttk.SECONDARY).pack(**cnf)
ttk.Radiobutton(rb_group, value=3, text="success", variable=radio_var,
                bootstyle=ttk.SUCCESS).pack(**cnf)
ttk.Radiobutton(rb_group, value=4, text="info", variable=radio_var,
                bootstyle=ttk.INFO).pack(**cnf)
ttk.Radiobutton(rb_group, value=5, text="warning", variable=radio_var,
                bootstyle=ttk.WARNING).pack(**cnf)
ttk.Radiobutton(rb_group, value=6, text="danger", variable=radio_var,
                bootstyle=ttk.DANGER).pack(**cnf)
ttk.Radiobutton(rb_group, value=7, text="disabled",
                variable=radio_var, state=ttk.DISABLED).pack(**cnf)


ttframe = ttk.Frame(lframe)
ttframe.pack(pady=5, fill=ttk.X, side=ttk.TOP)

# tableview
data = [
    ('South Island, New Zealand', 1),
    ('Paris', 2),
    ('Bora Bora', 3),
    ('Maui', 4),
    ('Tahiti', 5)
]

# treeview
tv = ttk.Treeview(ttframe, columns=[0, 1], show=ttk.HEADINGS)
for row in data:
    tv.insert('', 'end', values=row)
tv.selection_set('I001')
tv.heading(0, text='City')
tv.heading(1, text='Rank')
tv.pack(side=ttk.LEFT, anchor=ttk.NE, fill=ttk.BOTH, padx=(0, 2))


# # text widget
# txt = Text(ttframe, bootstyle=ROUNDED, height=5, width=50)
# txt.scrollbar.set(show_arrows=False)
# txt.insert(END, ZEN)
# txt.pack(side=RIGHT, anchor=NW, fill=BOTH, padx=(2, 0))

# # notebook with table and text tabs
nb = ttk.Notebook(lframe)
nb.pack(pady=5, fill=ttk.BOTH, expand=True)
nb_text = "This is a notebook tab.\nYou can put any widget you want here."
nb.add(ttk.Label(nb, text=nb_text), text="Tab 1", sticky=ttk.NW)
nb.add(ttk.Label(nb, text="A notebook tab."), text="Tab 2",
       sticky=ttk.NW)
nb.add(ttk.Frame(nb), text='Tab 3')
nb.add(ttk.Frame(nb), text='Tab 4')
nb.add(ttk.Frame(nb), text='Tab 5')

# ---------- SECTION 2 ------------------------------------------------

# button group
btn_group = ttk.Labelframe(rframe, text="Buttons", padding=10)
btn_group.pack(fill=ttk.X)

# menu button
menu = ttk.Menu(app)
for i, t in enumerate(app.theme.theme_names()):
    menu.add_radiobutton(label=t, value=i)
mb = ttk.Menubutton(btn_group, text="Menubutton", menu=menu)
mb.pack(fill=ttk.X, pady=5)


default = ttk.Button(btn_group, text="Default button")
default.pack(fill=ttk.X)
default.focus_set()
ob = ttk.Button(btn_group, text="Outline button", bootstyle=ttk.OUTLINE)
ob.pack(fill=ttk.X, pady=5)
lb = ttk.Button(btn_group, text="Link button", bootstyle=ttk.LINK)
lb.pack(fill=ttk.X, pady=5)

# ---------- SECTION 3 ------------------------------------------------

input_group = ttk.Labelframe(rframe, text="Other input widgets", padding=10)
input_group.pack(fill=ttk.X, pady=10)
ttk.Entry(input_group, text="entry widget").pack(fill=ttk.X)
ttk.Entry(input_group, text="password", show="•").pack(fill=ttk.X, pady=5)
ttk.Spinbox(input_group, from_=0, to=100, text=50).pack(fill=ttk.X)

lb = ttk.Listbox(input_group, values=app.theme.theme_names(), height=4)
lb.pack(fill=ttk.X, pady=5)
lb.activate(0)

# # vertical widgets
vframe = ttk.Frame(rframe)
vframe.pack(expand=ttk.YES, fill=ttk.BOTH)
cnf = {'fill': ttk.Y, 'padx': 5, 'side': ttk.LEFT, 'expand': ttk.YES}
s1 = ttk.Scale(vframe, orient=ttk.VERTICAL, value=50)
s1.pack(**cnf)
s1.bind_mousewheel()

ttk.Scale(vframe, orient=ttk.VERTICAL,
          bootstyle=ttk.SECONDARY, value=75).pack(**cnf)
ttk.Scrollbar(vframe, bootstyle=ttk.SUCCESS).pack(**cnf)
ttk.Scrollbar(vframe, bootstyle=ttk.INFO).pack(**cnf)
ttk.Progressbar(vframe, orient=ttk.VERTICAL, value=50,
                bootstyle=ttk.WARNING).pack(**cnf)
ttk.Progressbar(vframe, orient=ttk.VERTICAL, value=75,
                bootstyle=(ttk.DANGER, ttk.STRIPED)).pack(**cnf)

default.configure(command=lambda: lb.delete(1))

if __name__ == '__main__':

    app.mainloop()
