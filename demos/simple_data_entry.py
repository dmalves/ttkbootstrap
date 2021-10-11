import ttkbootstrap as ttk

app = ttk.Window(title="Simple data entry form")
app.resizable(False, False)
app.grid_columnconfigure(2, weight=1)

lbl = ttk.Label(app, text="Please enter your contact information", width=60)
lbl.grid(columnspan=3, pady=10, padx=5)


def print_results(e):
    for k, v in e.items():
        print(f'{k}: {v.get()}')


entries = {}
for i, lbl in enumerate(['Name', 'Address', 'Phone']):
    label = ttk.Label(app, text=lbl)
    label.grid(row=i + 1, sticky=ttk.EW, pady=10, padx=5)
    entry = ttk.Entry(app)
    entry.grid(row=i + 1, column=1, columnspan=2, sticky=ttk.EW, padx=5)
    entries[lbl] = entry

btn_cnf = {'sticky': ttk.EW, 'padx': 5, 'pady': (5, 10)}

btn_submit = ttk.Button(app, text='Submit', bootstyle=ttk.SUCCESS)
btn_submit['command'] = lambda: print_results(entries)
btn_submit.grid(row=4, **btn_cnf)
btn_submit.bind_return_key()

btn_quit = ttk.Button(app, text='Cancel', bootstyle=ttk.DANGER)
btn_quit['command'] = app.quit
btn_quit.grid(row=4, column=1, **btn_cnf)

app.mainloop()
