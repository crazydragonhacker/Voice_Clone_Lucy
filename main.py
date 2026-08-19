import tkinter as tk
from PIL import Image, ImageTk


# -----------------------------
# Window
# -----------------------------

window = tk.Tk()
window.title("AI Assistant")
window.geometry("500x700")


# -----------------------------
# Character
# -----------------------------

character_label = tk.Label(window)
character_label.pack(pady=20)


# -----------------------------
# Show Expression
# -----------------------------

def show_expression(expression):

    image = Image.open(f"character/{expression}.png")

    # Keep the original aspect ratio
    image.thumbnail((400, 500))

    character_image = ImageTk.PhotoImage(image)

    # Keep a reference to the image
    character_label.image = character_image

    # Change the displayed image
    character_label.config(image=character_image)


# -----------------------------
# Buttons
# -----------------------------

button_frame = tk.Frame(window)
button_frame.pack(pady=20)

tk.Button(
    button_frame,
    text="Neutral",
    command=lambda: show_expression("neutral")
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Happy",
    command=lambda: show_expression("happy")
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Sad",
    command=lambda: show_expression("sad")
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Angry",
    command=lambda: show_expression("angry")
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Surprised",
    command=lambda: show_expression("surprised")
).pack(side="left", padx=5)


# -----------------------------
# Start with Neutral
# -----------------------------

show_expression("neutral")


# -----------------------------
# Start Application
# -----------------------------

window.mainloop()