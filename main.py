import tkinter as tk
from PIL import Image, ImageTk
from ollama import chat


# -----------------------------
# Window
# -----------------------------

window = tk.Tk()
window.title("AI Assistant")
window.geometry("600x800")


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

    # Keep original aspect ratio
    image.thumbnail((400, 500))

    character_image = ImageTk.PhotoImage(image)

    # Keep reference to image
    character_label.image = character_image

    # Change displayed image
    character_label.config(image=character_image)


# -----------------------------
# Chat Area
# -----------------------------

chat_box = tk.Text(
    window,
    height=10,
    width=60,
    state="disabled"
)

chat_box.pack(pady=10)


# -----------------------------
# User Input
# -----------------------------

input_box = tk.Entry(
    window,
    width=50
)

input_box.pack(pady=5)


# -----------------------------
# Send Message
# -----------------------------

def send_message():

    user_message = input_box.get()

    if user_message == "":
        return

    # Display user's message
    chat_box.config(state="normal")

    chat_box.insert(
        tk.END,
        "You: " + user_message + "\n"
    )

    chat_box.config(state="disabled")

    # Clear input box
    input_box.delete(0, tk.END)


    # Send message to Gemma
    response = chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )


    # Get Gemma's response
    ai_response = response["message"]["content"]


    # Display AI response
    chat_box.config(state="normal")

    chat_box.insert(
        tk.END,
        "AI: " + ai_response + "\n\n"
    )

    chat_box.config(state="disabled")


# -----------------------------
# Send Button
# -----------------------------

send_button = tk.Button(
    window,
    text="Send",
    command=send_message
)

send_button.pack(pady=5)


# -----------------------------
# Start with Neutral Expression
# -----------------------------

show_expression("neutral")


# -----------------------------
# Start Application
# -----------------------------

window.mainloop()