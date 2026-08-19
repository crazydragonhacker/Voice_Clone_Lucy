import tkinter as tk
from PIL import Image, ImageTk
from ollama import chat
from piper import PiperVoice
import wave
import winsound

voice = PiperVoice.load("en_US-amy-medium.onnx")

# -----------------------
#Create a voice function
# -----------------------

def speak(text):

    with wave.open("response.wav", "wb") as wav_file:

        voice.synthesize_wav(text, wav_file)

    winsound.PlaySound(
        "response.wav",
        winsound.SND_FILENAME
    )


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
            "role": "system",
            "content": """
    You are an AI assistant with an anime-style character.

    For every response, you MUST return exactly this format:

    EMOTION: <emotion>
    RESPONSE: <response>

    The emotion MUST be one of:

    neutral
    happy
    sad
    angry
    surprised

    Choose the emotion that best matches the response.

    Do not use any other emotion names.
    Do not add anything before EMOTION.
    Do not add anything after the response.
    """
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )


    # Get Gemma's response
    ai_response = response["message"]["content"]


    # -----------------------------
    # Extract emotion
    # -----------------------------

    lines = ai_response.splitlines()

    emotion = "neutral"
    response_text = ""


    for line in lines:

        if line.startswith("EMOTION:"):
            emotion = line.replace("EMOTION:", "").strip()

        elif line.startswith("RESPONSE:"):
            response_text = line.replace("RESPONSE:", "").strip()


    # -----------------------------
    # Change character expression
    # -----------------------------

    show_expression(emotion)


    # Display AI response
    chat_box.config(state="normal")

    chat_box.insert(
        tk.END,
        "Chihaya: " + response_text + "\n\n"
    )

    chat_box.config(state="disabled")

    speak(response_text)


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