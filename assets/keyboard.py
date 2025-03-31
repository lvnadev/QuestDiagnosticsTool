import tkinter as tk
import subprocess

def send_keyevent(keycode):
    command = f"adb shell input keyevent {keycode}"
    subprocess.run(command, shell=True)

def on_key_press(event):
    char = event.keysym.lower()
    if char in key_map:
        keycode = key_map[char]
        send_keyevent(keycode)
        highlight_key(keycode, True)

def on_key_release(event):
    char = event.keysym.lower()
    if char in key_map:
        keycode = key_map[char]
        highlight_key(keycode, False)

def highlight_key(keycode, active):
    for btn, code in key_buttons.items():
        if code == keycode:
            btn.config(relief=tk.SUNKEN if active else tk.RAISED)
            break

def create_keyboard(root):
    keys = [
        [("`", 68), ("1", 8), ("2", 9), ("3", 10), ("4", 11), ("5", 12), ("6", 13), ("7", 14), ("8", 15), ("9", 16), ("0", 7), ("-", 69), ("=", 70), ("Backspace", 67)],
        [("Tab", 61), ("Q", 45), ("W", 51), ("E", 33), ("R", 46), ("T", 48), ("Y", 53), ("U", 49), ("I", 37), ("O", 43), ("P", 44), ("[", 71), ("]", 72), ("\\", 73)],
        [("Caps", 115), ("A", 29), ("S", 47), ("D", 32), ("F", 34), ("G", 35), ("H", 36), ("J", 38), ("K", 39), ("L", 40), (";", 74), ("'", 75), ("Enter", 66)],
        [("Shift", 59), ("Z", 54), ("X", 52), ("C", 31), ("V", 50), ("B", 30), ("N", 42), ("M", 41), (",", 55), (".", 56), ("/", 76), ("Shift", 60)],
        [("Ctrl", 113), ("Alt", 57), ("Space", 62), ("Alt", 58), ("Ctrl", 114)]
    ]
    
    global key_map, key_buttons
    key_map = {k.lower(): v for row in keys for k, v in row}
    key_buttons = {}
    
    for row_index, row in enumerate(keys, start=2):
        col_index = 0
        for key, keycode in row:
            width = 5 if key not in ["Backspace", "Tab", "Caps", "Enter", "Shift", "Ctrl", "Alt", "Space"] else 10
            btn = tk.Button(root, text=key, width=width, height=2, command=lambda k=keycode: send_keyevent(k))
            btn.grid(row=row_index, column=col_index, columnspan=2 if width == 10 else 1)
            key_buttons[btn] = keycode
            col_index += 2 if width == 10 else 1

root = tk.Tk()
root.title("Quest 2 ADB Keyboard")
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)
create_keyboard(root)
root.mainloop()
