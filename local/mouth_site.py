import pyautogui as pag
import tkinter as tk


def get_site():
    site = pag.position()
    return site


def print_down(*event):
    x, y = get_site()
    print("X : {}\nY : {}".format(x, y))


class MouthSite:
    def __init__(self):
        self.windows = tk.Tk()
        self.windows.title = "MouthSite"
        self.windows.geometry('100x90')
        self.windows.resizable(False, False)

        self.frame1 = tk.Frame(self.windows)
        self.frame2 = tk.Frame(self.windows)
        self.frame3 = tk.Frame(self.windows)

        self.label1 = tk.Label(self.frame1, text="X :", width=5, height=1)
        self.label2 = tk.Label(self.frame2, text="Y :", width=5, height=1)

        self.text1 = tk.Text(self.frame1, width=5, height=1)
        self.text2 = tk.Text(self.frame2, width=5, height=1)

        self.button = tk.Button(self.frame3, text="保存", command=print_down, width=5, height=1)

        self.button.bind_all("<Return>", print_down)

        self.button.grid(row=0, column=1, padx=3, pady=1)
        self.text1.grid(row=0, column=2, padx=5, pady=1)
        self.text2.grid(row=0, column=2, padx=5, pady=1)
        self.label1.grid(row=0, column=1, padx=3, pady=1)
        self.label2.grid(row=0, column=1, padx=3, pady=1)
        self.frame1.grid(row=0, column=1)
        self.frame2.grid(row=1, column=1)
        self.frame3.grid(row=2, column=1)

    def start(self):
        self.windows.after(1, self.refresh_text)
        self.windows.mainloop()

    def refresh_text(self):
        x, y = get_site()
        self.text1.delete(0.0, tk.END)
        self.text2.delete(0.0, tk.END)
        self.text1.insert(tk.INSERT, x)
        self.text2.insert(tk.INSERT, y)
        self.text1.update()
        self.text2.update()
        self.windows.after(1, self.refresh_text)


if __name__ == '__main__':
    mouth = MouthSite()
    mouth.start()
