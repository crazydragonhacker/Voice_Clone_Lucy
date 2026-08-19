
import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()
window.title("AI Assistant")
window.geometry("500x700")

# Load image
image = Image.open("character/neutral.png")

# Resize while keeping the original aspect ratio
image.thumbnail((400, 500))

character_image = ImageTk.PhotoImage(image)

character_label = tk.Label(window, image=character_image)
character_label.pack(pady=20)

window.mainloop()