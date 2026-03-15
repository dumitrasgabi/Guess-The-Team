from ui import GuessTheTeam
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    app = GuessTheTeam(root)
    root.mainloop()
