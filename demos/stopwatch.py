import ttkbootstrap as ttk


class Stopwatch(ttk.Window):
    def __init__(self):
        super().__init__(title="Stopwatch Demo", theme="cosmo", 
                         resizable=False)
        self.running = ttk.Variable(value=False)
        self.elapsed = ttk.Variable(value=0)

        # arrange layout
        self.stopwatch_lbl = ttk.Label(
            self, text="00:00:00", font="-size 32", anchor=ttk.CENTER
        )
        self.stopwatch_lbl.pack(side=ttk.TOP, padx=60, pady=20)

        self.btn_start = ttk.Button(
            self,
            text="Start",
            bootstyle=ttk.INFO,
            command=self.toggle,
        )
        self.btn_start.pack(side=ttk.LEFT, fill=ttk.X,
                            padx=5, pady=5, expand=True)
        self.btn_start.focus_set()
        self.btn_start.bind_return_key()

        self.btn_reset = ttk.Button(
            self,
            text="Reset",
            bootstyle=ttk.SUCCESS,
            command=self.reset,
        )
        self.btn_reset.pack(side=ttk.LEFT, fill=ttk.X,
                            padx=5, pady=5, expand=True)

        self.btn_quit = ttk.Button(
            self, text="Quit", bootstyle=ttk.DANGER, command=self.quit,
        )
        self.btn_quit.pack(side=ttk.LEFT, fill=ttk.X,
                           padx=5, pady=5, expand=True)

    def pause(self):
        self.after_cancel(self._eventid)

    def increment(self):
        current = self.elapsed.get() + 1
        self.elapsed.set(current)
        time_str = "{:02d}:{:02d}:{:02d}".format(
            (current // 100) // 60, (current // 100) % 60, current % 100
        )

        self.stopwatch_lbl["text"] = time_str
        self._eventid = self.after(10, self.increment)

    def start(self):
        self._eventid = self.after(1, self.increment)

    def reset(self):
        self.elapsed.set(0)
        self.stopwatch_lbl["text"] = "00:00:00"

    def toggle(self):
        if self.running.get():
            self.pause()
            self.running.set(False)
            self.btn_start.configure(text="Start", bootstyle=ttk.INFO)
        else:
            self.start()
            self.running.set(True)
            self.btn_start.configure(
                text="Pause", bootstyle=(ttk.INFO, ttk.OUTLINE))


if __name__ == "__main__":

    Stopwatch().mainloop()
