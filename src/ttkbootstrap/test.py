from tkinter import ttk
import tkinter as tk
from theme import Theme
from constants import *

from widgets import Window
from widgets import Button, Checkbutton
from widgets import Combobox, Entry
from widgets import Frame, Label, Labelframe
from widgets import Listbox, Menu, Menubutton
from widgets import Notebook, Panedwindow, Progressbar
from widgets import Radiobutton, Scale, Scrollbar
from widgets import Separator, Sizegrip

window = Window(theme='superhero')

btn = Button(window, 'success', text="Hello World!")
btn.pack(padx=10, pady=10)

btn2 = Button(window, 'success', text="Hello Again!",
              command=lambda: window.theme.use('flatly'))
btn2.pack(padx=10, pady=10)

btn2.configure(bootstyle='danger')

btn3 = Button(window, 'success-outline', text="Hello Outline!",
              command=lambda: window.theme.use('flatly'))
btn3.pack(padx=10, pady=10)

btn4 = Button(window, 'danger-link', text="Hello Link!",
              command=lambda: window.theme.use('cosmo'))
btn4.pack(padx=10, pady=10)

# cb1 = Checkbutton(window, text='Option 1', bootstyle='danger')
# cb1.pack(padx=10, pady=10)

# cb2 = Checkbutton(window, text='Option 2', bootstyle='rounded')
# cb2.pack(padx=10, pady=10)

# cb3 = Checkbutton(window, text='Option 3', bootstyle='rounded')
# cb3.pack(padx=10, pady=10)

# cb3 = Checkbutton(window, text='Option 3', bootstyle='rounded', state=DISABLED)
# cb3.pack(padx=10, pady=10)

# cb4 = Checkbutton(window, text='Option 4', bootstyle='warning-toolbutton')
# cb4.pack(padx=10, pady=10)

# cb5 = Checkbutton(window, text='Option 5', bootstyle='outline-danger-toolbutton')
# cb5.pack(padx=10, pady=10)

# cbo = Combobox(window, values=list(range(20)), height=10, bootstyle=WARNING)
# cbo.pack(padx=10, pady=10)
# cbo.current(0)

# entry = Entry(window)
# entry.insert('end', 'Hello World')
# entry.pack(padx=10, pady=10)

# frame1 = Frame(window, width=200, height=200, bootstyle='success')
# frame1.pack(padx=10, pady=10)

# frame2 = Frame(window, width=100, height=100, bootstyle='danger-focusframe')
# frame2.pack(padx=10, pady=10)

# Label(window, text="Regular").pack(padx=10, pady=10)
# Label(window, text="success", bootstyle="success").pack(padx=10, pady=10)
# Label(window, text="inverse", bootstyle=(
#     'inverse', 'success')).pack(padx=10, pady=10)

# Labelframe(window, text="My Frame", width=100, height=100).pack(padx=10, pady=10)

# lb = Listbox(window)
# for x in range(1, 5):
#     lb.insert('', 'end', values=[x])
# lb.pack(padx=10, pady=10)

# Menubutton(window, text="Push to see").pack(padx=10, pady=10)
# Menubutton(window, text="Push to see",
#            bootstyle='outline').pack(padx=10, pady=10)

# nb = Notebook(window, width=100, height=100)
# nb.add(Frame(nb), text="Tab 1")
# nb.add(Frame(nb), text="Tab 2")
# nb.pack(padx=10, pady=10)

# pw = Panedwindow(window, bootstyle=SUCCESS, orient=HORIZONTAL)
# pw.pack(padx=10, pady=10, fill=BOTH, expand=YES)
# pw.insert('end', Frame(window, width=200, height=200))
# pw.insert('end', Frame(window, width=200, height=200))

# pb = Progressbar(window, value=25, orient=VERTICAL)
# pb.pack(padx=10, pady=10, fill=Y)
# pb.start()

# pb2 = Progressbar(window, value=25, orient=HORIZONTAL,
#                   bootstyle=(SUCCESS, STRIPED))
# pb2.pack(padx=10, pady=10, fill=X)
# pb2.start()

# var = tk.Variable()
# Radiobutton(window, text='Option 1', value=1,
#             variable=var).pack(padx=10, pady=10)
# Radiobutton(window, text='Option 2', value=2,
#             variable=var, bootstyle=WARNING).pack(padx=10, pady=10)
# Radiobutton(window, text='Option 3', value=3,
#             variable=var).pack(padx=10, pady=10)

# s = Scale(window, from_=0, to=100)
# s.pack(padx=10, pady=10, fill=X)
# s.bind_mousewheel(10)

# Button(window, text='Bind MouseWheel', command=s.bind_mousewheel).pack(padx=10, pady=10)
# Button(window, text='Unbind MouseWheel', command=s.unbind_mousewheel).pack(padx=10, pady=10)

# Scale(window, from_=0, to=100, orient=HORIZONTAL).pack(
#     padx=10, pady=10, fill=X, expand=YES)

# sb = Scrollbar(window, orient=HORIZONTAL, thickness=15)
# sb.pack(padx=10, pady=10, fill=X)
# sb.set(0.1, 0.3)

# sb = Scrollbar(window)
# sb.pack(padx=10, pady=10, fill=Y, expand=YES)
# sb.set(0.1, 0.3)

# Separator(window, orient=VERTICAL).pack(padx=10, pady=10, fill=Y, expand=YES)
# Sizegrip(window).pack(fill=BOTH, expand=YES)

window.mainloop()
