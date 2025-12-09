import tkinter as tk
from tkinter import ttk

import pyttsx3
import threading


def create_window() -> tk.Tk:
    root = tk.Tk()
    # width x height + width_padding + height_padding
    root.geometry("800x600+600+300")

    return root


def setup_title(root: tk.Tk):

    title = "* * Python * *"
    colors = ["#e6194b","#3cb44b"] 
    flick_interval = 500

    frame = tk.Frame(root, bg="white")
    frame.pack(side="top", pady=10)

    labels = []

    # Store each letter in it's own Label
    # this way, we can easily cycle through colors
    start_color_index = 0
    for i, ch in enumerate(title):
        label = tk.Label(frame, text=ch, font=("Cascadia", 28))
        label.pack(side="left")

        # we ignore whitespaces
        if title[i] == " ":
            color_index = 0
        else:
            color_index = start_color_index
            start_color_index = (start_color_index + 1) % len(colors)

        labels.append([label, color_index])

    def title_color_flicker():

        for label, color_index in labels:
            label.config(fg=colors[color_index])
        
        for e, (label, color_index) in enumerate(labels):
            label.config(fg=colors[color_index])

            labels[e][1] = (color_index + 1) % len(colors)

        root.after(flick_interval, title_color_flicker)

    title_color_flicker()


def setup_globes(root: tk.Tk):
    canvas = tk.Canvas(root, width=420, height=180, highlightthickness=0)
    canvas.pack(side="top")

    colors = ["red", "green"]
    selected_color = 0

    ovals = []
    oval_size = 30
    oval_distance = 20

    # left side
    height_start = 20
    width_start = 50
    for i in range(3):
        
        w0 = width_start
        h0 = height_start + i * oval_size + i*oval_distance
        w1 = w0 + oval_size
        h1 = h0 + oval_size

        oval = canvas.create_oval(w0, h0, w1, h1, fill=colors[selected_color])
        ovals.append(oval)

        selected_color = (selected_color + 1) % len(colors)

    # right side
    height_start = 20
    width_start = 370
    for i in range(3):
        
        w0 = width_start
        h0 = height_start + i * oval_size + i*oval_distance
        w1 = w0 + oval_size
        h1 = h0 + oval_size

        oval = canvas.create_oval(w0, h0, w1, h1, fill=colors[selected_color])
        ovals.append(oval)

        selected_color = (selected_color + 1) % len(colors)
    

    scale = 0.8

    def globles_animation():
        nonlocal scale
        scale = 1 / scale
        
        for item in ovals:
            
            x1, y1, x2, y2 = canvas.coords(item)
            cx = x1  # use left corner as anchor to avoid drift
            cy = y1
            canvas.scale(item, cx, cy, scale, scale)

        root.after(500, globles_animation)

    globles_animation()

def setup_button_and_combobox(root: tk.Tk):

    combo = ttk.Combobox(root, values=["Merry Christmas!", "Ho ho ho!", "Happy Holidays"], state="readonly")
    combo.set("Ho ho ho!")
    combo.pack(side="top", pady=10)

    def tts_combobox():
        text = combo.get()
        pyttsx3.speak(text)

    def thread_tts_combobox():
        '''
        Runs the tts_combobox function on a separte thread.
        This avoid GUI freezes
        '''

        threading.Thread(target=tts_combobox, daemon=True).start()

    # btn = tk.Button(root, text="Let's hear it!", width=50, command=tts_combobox)
    btn = tk.Button(root, text="Let's hear it!", width=50, command=thread_tts_combobox)
    btn.pack(side="top", pady=10)


if __name__ == "__main__":
    root = create_window()
    setup_title(root)
    setup_globes(root)
    setup_button_and_combobox(root)

    root.mainloop()