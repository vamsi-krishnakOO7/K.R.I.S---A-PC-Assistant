import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """Get the absolute path to the resource, works for development and for PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def initialize_ui():
    global ui_root, ui_text
    ui_root = tk.Tk()
    ui_root.title("INSERT TITLE - ASSISTANT ABBREVATION/NAME")

    # Set window size and position
    ui_root.geometry("500x130+750+500")
    
    theme_color = "#333333"
    text_color = "#FFFFFF"
    ui_root.configure(bg=theme_color)
    
    content_frame = tk.Frame(ui_root, bg=theme_color)
    content_frame.pack(expand=True, fill='both', padx=10, pady=10)
    
    original_image_path = resource_path('resources/ai.png')
    original_image = Image.open(original_image_path)
    resized_image = original_image.resize((100, 100))
    gif_image = ImageTk.PhotoImage(resized_image)
    
    gif_label = tk.Label(content_frame)
    gif_label.pack(side=tk.LEFT, padx=10)
    gif_label.config(image=gif_image)
    gif_label.image = gif_image

    # Create a Scrollbar and associate it with ui_text
    scrollbar = tk.Scrollbar(content_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a Text widget
    ui_text = tk.Text(content_frame, height=24, width=80, yscrollcommand=scrollbar.set, wrap='word', bg=theme_color, fg=text_color, insertbackground=text_color)
    ui_text.pack(side=tk.LEFT,expand=True, fill='both')

    scrollbar.config(command=ui_text.yview, bg=theme_color)
    
    return ui_root, ui_text

def update_ui(message):
    def do_update():
        ui_text.config(state=tk.NORMAL)
        ui_text.insert(tk.END, message + '\n\n')
        ui_text.config(state=tk.DISABLED)
        ui_text.see(tk.END)
    ui_root.after(0, do_update)