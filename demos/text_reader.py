import freestyle as fs
from tkinter import filedialog


def open_file():
    path = filedialog.askopenfilename()
    if not path:
        return

    with open(path, encoding='utf-8') as f:
        txt.delete("1.0", fs.END)
        txt.insert(fs.END, f.read())
        ent['text'] = path


app = fs.Window(title="Text Reader", theme="minty")

txt = fs.Text(app, freestyle=fs.ROUNDED)
txt.pack_set(fill=fs.BOTH, expand=fs.YES, padx=5, pady=5)
txt.scrollbar.set(show_arrows=False)

ent = fs.Entry(app)
ent.pack_set(side=fs.LEFT, fill=fs.X, expand=fs.YES, padx=(5, 0), pady=(2, 5))

btn = fs.Button(app, text="Browse", command=open_file)
btn.pack_set(side=fs.RIGHT, fill=fs.X, padx=5, pady=(2, 5))

app.run()
