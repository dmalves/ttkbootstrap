import ttkbootstrap as ttk
from random import randint, random


app = ttk.Window("Equalizer", "darkly")

controls = ["VOL", "31.25", "62.5", "125", "250", "500", "1K", "2K", "4K",
            "8K", "16K", "GAIN"]


def update_label(*args):
    print(args)


for control in controls:

    # slider container with label
    container = ttk.Frame(app, padding=5)
    container.pack(side=ttk.LEFT, fill=ttk.Y, padx=10)
    lbl = ttk.Label(container, text=control, anchor=ttk.CENTER,
                    font='TkHeadingFont')
    lbl.pack(side=ttk.TOP, fill=ttk.X, pady=10)

    start_val = randint(0, 100)

    # slider widget
    scale_style = ttk.SUCCESS if control in ["VOL", "GAIN"] else ttk.INFO
    s = ttk.Scale(container, orient=ttk.VERTICAL, from_=100, to=0,
                  value=start_val, bootstyle=scale_style)
    s.pack(fill=ttk.Y)
    s.bind_mousewheel(increment=2)

    # label to contain slider value
    val = ttk.Label(container, text=control, textvariable=s.variable)
    val.pack(pady=10)

app.mainloop()
