from PIL.Image import register_save
import ttkbootstrap as ttk
from tkinter import filedialog


def open_file():
    path = filedialog.askopenfilename()
    if not path:
        return

    with open(path, encoding='utf-8') as f:
        txt.delete("1.0", ttk.END)
        txt.insert(ttk.END, f.read())
        ent['text'] = path


app = ttk.Window(title="Text Reader", theme="superhero", resizable=False)

txt = ttk.Text(app, bootstyle=ttk.ROUNDED)
txt.pack(side=ttk.TOP, fill=ttk.BOTH, expand=ttk.YES, padx=5, pady=5)

ent = ttk.Entry(app)
ent.pack(side=ttk.LEFT, fill=ttk.X, expand=ttk.YES, padx=(5, 0), pady=(2, 5))


btn = ttk.Button(app, text="Browse", command=open_file)
btn.pack(side=ttk.RIGHT, fill=ttk.X, padx=5, pady=(2, 5))

app.mainloop()
