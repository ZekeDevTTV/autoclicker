import threading
import time
import tkinter as tk
from tkinter import ttk
from pynput import mouse, keyboard

clicking = False
running = True
delay = 0.1
mode = "keyboard"
selected_input = "e"

toggle_key = keyboard.Key.f7

mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

def loop():
    global clicking
    while running:
        if clicking:
            if mode == "mouse":
                if selected_input == "left":
                    mouse_controller.click(mouse.Button.left)
                elif selected_input == "right":
                    mouse_controller.click(mouse.Button.right)

            elif mode == "keyboard":
                try:
                    keyboard_controller.press(selected_input)
                    keyboard_controller.release(selected_input)
                except:
                    pass

            time.sleep(delay)
        else:
            time.sleep(0.01)

def on_press(key):
    global clicking
    if key == toggle_key:
        clicking = not clicking
        status_var.set("ON" if clicking else "OFF")

listener = keyboard.Listener(on_press=on_press)
listener.start()

root = tk.Tk()
root.title("Autoclicker")
root.geometry("520x520")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")

style.configure(".",
    background="#1e1e1e",
    foreground="#ffffff",
    fieldbackground="#2a2a2a"
)

style.configure("TButton",
    background="#2a2a2a",
    foreground="#ffffff",
    padding=6
)

style.map("TButton",
    background=[("active", "#3a3a3a")]
)

style.configure("Selected.TButton",
    background="#4CAF50",
    foreground="#ffffff"
)

style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
style.configure("TLabelframe", background="#1e1e1e", foreground="#ffffff")
style.configure("TLabelframe.Label", background="#1e1e1e", foreground="#ffffff")

header = ttk.Frame(root)
header.pack(fill="x", pady=10)

status_var = tk.StringVar(value="OFF")
ttk.Label(header, text="Status:", font=("Segoe UI", 10)).pack(side="left", padx=5)
ttk.Label(header, textvariable=status_var, font=("Segoe UI", 10, "bold")).pack(side="left")

ttk.Label(header, text="Toggle: F7").pack(side="right")

settings = ttk.LabelFrame(root, text="Settings")
settings.pack(fill="x", padx=10, pady=10)

ttk.Label(settings, text="Delay").grid(row=0, column=0, padx=5, pady=5)

delay_entry = ttk.Entry(settings, width=10)
delay_entry.insert(0, "0.1")
delay_entry.grid(row=0, column=1)

def set_delay():
    global delay
    try:
        delay = float(delay_entry.get())
    except:
        pass

ttk.Button(settings, text="Apply", command=set_delay).grid(row=0, column=2, padx=5)

selected_var = tk.StringVar(value="Selected: e")
ttk.Label(settings, textvariable=selected_var).grid(row=1, column=0, columnspan=3, pady=5)

input_frame = ttk.Frame(root)
input_frame.pack(fill="both", expand=True, padx=10)

keyboard_frame = ttk.LabelFrame(input_frame, text="Keyboard")
keyboard_frame.pack(fill="both", expand=True, pady=5)

keys_layout = [
    list("1234567890"),
    list("qwertyuiop"),
    list("asdfghjkl"),
    list("zxcvbnm")
]

selected_button = None

def set_key(k, btn):
    global selected_input, mode, selected_button
    selected_input = k
    mode = "keyboard"
    selected_var.set(f"Selected: {k}")

    if selected_button:
        selected_button.config(style="TButton")

    btn.config(style="Selected.TButton")
    selected_button = btn

for r, row in enumerate(keys_layout):
    for c, k in enumerate(row):
        btn = ttk.Button(keyboard_frame, text=k, width=4)
        btn.grid(row=r, column=c, padx=3, pady=3)
        btn.config(command=lambda key=k, b=btn: set_key(key, b))

space_btn = ttk.Button(keyboard_frame, text="SPACE", width=30)
space_btn.grid(row=5, column=0, columnspan=10, pady=8)
space_btn.config(command=lambda: set_key(" ", space_btn))

mouse_frame = ttk.LabelFrame(input_frame, text="Mouse")
mouse_frame.pack(fill="x", pady=5)

def set_mouse(btn):
    global selected_input, mode
    selected_input = btn
    mode = "mouse"
    selected_var.set(f"Selected: {btn} click")

ttk.Button(mouse_frame, text="Left Click", command=lambda: set_mouse("left")).pack(side="left", padx=10, pady=5)
ttk.Button(mouse_frame, text="Right Click", command=lambda: set_mouse("right")).pack(side="left", padx=10, pady=5)

thread = threading.Thread(target=loop)
thread.daemon = True
thread.start()

def on_close():
    global running
    running = False
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
