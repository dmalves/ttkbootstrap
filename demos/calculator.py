import ttkbootstrap as ttk


def number_press(display: ttk.Label, key):
    new_text = int(str(display["text"]) + str(key))
    display["text"] = new_text


def clear_press(display: ttk.Label):
    display["text"] = 0


app = ttk.Window("Calculator", "flatly", resizable=False)

mframe = ttk.Frame(app, padding=5)
mframe.pack(fill=ttk.BOTH, expand=ttk.YES)

num_display = ttk.Label(mframe, text=0, font="TkFixedFont 20", anchor=ttk.E)
num_display.grid(columnspan=4, sticky=ttk.EW, pady=15, padx=10)

button_layout = [
    ("%", "C", "CE", "/"),
    (7, 8, 9, "*"),
    (4, 5, 6, "-"),
    (1, 2, 3, "+"),
    ("±", 0, ".", "="),
]

cnf = {"padding": 20, "width": 2}  # shared configuration

for i, row in enumerate(button_layout):
    for j, lbl in enumerate(row):
        if isinstance(lbl, int):
            b = ttk.Button(
                mframe,
                text=lbl,
                command=lambda d=num_display, k=i: number_press(d, k),
                **cnf
            )
            b.bind_return_key()
        elif lbl == "=":
            b = ttk.Button(mframe, text=lbl, bootstyle=ttk.SUCCESS, **cnf)
        elif lbl in ("C", "CE"):
            b = ttk.Button(
                mframe,
                text=lbl,
                bootstyle=ttk.SECONDARY,
                command=lambda: clear_press(num_display),
                **cnf
            )
        else:
            b = ttk.Button(mframe, text=lbl, bootstyle=ttk.SECONDARY, **cnf)
        b.grid(row=i + 1, column=j, sticky=ttk.NSEW, padx=1, pady=1)


if __name__ == "__main__":

    app.mainloop()
