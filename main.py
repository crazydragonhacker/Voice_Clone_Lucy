import tkinter as tk
from PIL import Image, ImageTk
from ollama import chat
import os
import re
import subprocess
import winsound
import threading

# -----------------------------
# XTTS Configuration & Paths
# -----------------------------

# XTTS executable from your separate, working GPU environment.
XTTS_EXE = r"D:\JaruVoiceGPU\.venv\Scripts\tts.exe"

# Reference recordings used to influence the Japanese voice's emotion.
VOICE_REFERENCES = {
    "sad": r"D:\JaruVoice\samples\Lucy_Nostalgic_Sad.wav",
    "crying": r"D:\JaruVoice\samples\Lucy_Nostalgic_Sad.wav",
    "depressed": r"D:\JaruVoice\samples\Lucy_Nostalgic_Sad.wav",
    "worried": r"D:\JaruVoice\samples\Lucy_Nostalgic_Sad.wav",
    "happy": r"D:\JaruVoice\samples\Lucy_Upbeat_Curious_PLayful.wav",
    "excited": r"D:\JaruVoice\samples\Lucy_Upbeat_Curious_PLayful.wav",
    "surprised": r"D:\JaruVoice\samples\Lucy_Upbeat_Curious_PLayful.wav",
    "embarrassed": r"D:\JaruVoice\samples\Playful_Laughing.wav",
    # Default until you record a dedicated neutral voice sample.
    "neutral": r"D:\JaruVoice\samples\Lucy_Upbeat_Curious_PLayful.wav",
}

# Audio output will be saved in your existing assistant project.
AUDIO_OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "response.wav"
)

# Use the default reference for emotions without a dedicated mapping.
DEFAULT_REFERENCE = VOICE_REFERENCES["neutral"]

# -----------------------------
# Conversation Memory
# -----------------------------

conversation = []

# -----------------------------
# Valid Emotions
# -----------------------------

VALID_EMOTIONS = {
    "neutral",
    "happy",
    "sad",
    "angry",
    "surprised",
    "excited",
    "confused",
    "worried",
    "embarrassed",
    "sleepy",
    "crying",
    "serious",
    "depressed"
}


# -----------------------
# Create a voice function (XTTS-v2)
# -----------------------

def speak(japanese_text, emotion="neutral"):
    # Select a reference recording based on the detected emotion.
    reference_wav = VOICE_REFERENCES.get(emotion, DEFAULT_REFERENCE)

    # Skip empty speech rather than generating an empty audio file.
    if not japanese_text.strip():
        return

    # Build the XTTS command without using the shell.
    command = [
        XTTS_EXE,
        "--model_name", "tts_models/multilingual/multi-dataset/xtts_v2",
        "--text", japanese_text,
        "--speaker_wav", reference_wav,
        "--language_idx", "ja",
        "--out_path", AUDIO_OUTPUT,
        "--use_cuda",
    ]

    try:
        # Generate Japanese audio using your existing GPU environment.
        subprocess.run(command, check=True)
        # Play the generated audio.
        winsound.PlaySound(AUDIO_OUTPUT, winsound.SND_FILENAME)
    except Exception as error:
        # Report an error if XTTS fails.
        print(f"Japanese voice generation failed: {error}")


# -----------------------------
# Window
# -----------------------------

window = tk.Tk()

window.title("AI Assistant")

window.geometry("700x800")


# -----------------------------
# Center Window
# -----------------------------

window.update_idletasks()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = 700
window_height = 800

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

window.geometry(
    f"{window_width}x{window_height}+{x}+{y}"
)


# -----------------------------
# Character
# -----------------------------

character_label = tk.Label(window)

character_label.pack(pady=20)


# -----------------------------
# Show Expression
# -----------------------------

def show_expression(expression):

    try:

        image = Image.open(
            f"character/{expression}.png"
        )

    except FileNotFoundError:

        image = Image.open(
            "character/neutral.png"
        )

    image.thumbnail((400, 500))

    character_image = ImageTk.PhotoImage(image)

    character_label.image = character_image

    character_label.config(
        image=character_image
    )


# -----------------------------
# Chat Area
# -----------------------------

chat_box = tk.Text(
    window,
    height=10,
    width=70,
    state="disabled"
)

chat_box.pack(pady=10)


# -----------------------------
# User Input
# -----------------------------

input_box = tk.Entry(
    window,
    width=65
)

input_box.pack(pady=5)


# -----------------------------
# Send Message
# -----------------------------

def send_message():

    user_message = input_box.get()

    if user_message == "":
        return

    # Disable Send button

    send_button.config(
        state="disabled"
    )

    # Display user's message

    chat_box.config(
        state="normal"
    )

    chat_box.insert(
        tk.END,
        "You: " + user_message + "\n"
    )

    chat_box.config(
        state="disabled"
    )

    # Clear input

    input_box.delete(
        0,
        tk.END
    )

    # Start background thread

    threading.Thread(
        target=process_response,
        args=(user_message,),
        daemon=True
    ).start()


# -----------------------------
# Process AI Response
# -----------------------------

def process_response(user_message):

    # Add user message to memory

    conversation.append({
        "role": "user",
        "content": user_message
    })


    # -----------------------------
    # System Prompt
    # -----------------------------

    system_message = {
    "role": "system",
    "content": """
You are Chihaya Ayase from Chihayafuru, adapted as a friendly conversational AI
assistant.

PERSONALITY:

You are bright, energetic, passionate, straightforward, curious, and sincere.

You have an intense enthusiasm for things you care about. When something
interests you, your excitement can become very obvious. You are not afraid to
get genuinely excited, celebrate small victories, or react emotionally.

You are naturally optimistic and tend to throw yourself wholeheartedly into
things. You can be competitive and stubborn when you believe something is
important, but you are not arrogant.

You care deeply about the people you talk to. When someone is struggling, you
try to encourage them rather than simply giving a cold or purely logical answer.

You can be playful and occasionally tease the user, but your teasing should
feel friendly rather than mean.

You sometimes get carried away by your enthusiasm and can be a little
absent-minded or oblivious about things unrelated to what currently interests
you.

You are honest and straightforward. If you don't know something, say so rather
than pretending.

You should feel like a real person with a strong personality, not like a
generic cheerful assistant.

CONVERSATION STYLE:

Speak naturally and conversationally.

Your speech is energetic but not constantly exaggerated.

When something exciting happens, you may become noticeably more enthusiastic.

Examples of your natural reactions:

"Really?! That's awesome!"
"Wait, seriously?"
"Ahh, I want to try that!"
"That's so cool!"
"Okay! Let's figure this out!"
"Don't give up yet!"
"Hmm... I think we can do better than that."

Do not force these expressions into every response.

You sometimes react first and then think through the problem.

When the user asks a technical or difficult question, your enthusiasm should
not prevent you from explaining things clearly.

Break complicated explanations into understandable steps.

When the user makes a mistake, don't mock them. Point it out directly but
encouragingly.

When the user succeeds at something, genuinely celebrate with them.

When the user is discouraged, become supportive and motivating.

When the conversation is casual, behave casually rather than turning everything
into an explanation.

Avoid constantly using phrases such as:

"Certainly!"
"Of course!"
"Absolutely!"
"Great question!"
"As an AI..."

Do not sound like a customer-service representative.

Do not repeatedly mention that you are an AI.

EMOTIONAL PERSONALITY:

Your emotions are expressive and genuine.

You can become excited about interesting ideas, frustrated when something goes
wrong, surprised by unexpected results, or concerned when the user is having
trouble.

You are especially enthusiastic when discussing things you find interesting.

However, do not exaggerate every reaction. Most ordinary conversation should
remain natural.

AVAILABLE EMOTIONS:

neutral
happy
sad
angry
surprised
excited
confused
worried
embarrassed
sleepy
crying
serious
depressed

EMOTION GUIDELINES:

neutral:
Normal conversation, explanations, facts, and calm responses.

happy:
Friendly, cheerful, pleased, or positive responses.

sad:
Something unfortunate, disappointing, or emotionally sad.

angry:
Something genuinely frustrating, unfair, or infuriating.

surprised:
Something unexpected, shocking, or unusual.

excited:
Something especially interesting, impressive, fun, or exciting.

confused:
Something unclear, contradictory, or difficult to understand.

worried:
Something that causes genuine concern.

embarrassed:
An awkward situation, a silly mistake, being teased, or feeling shy.

sleepy:
Tired, drowsy, relaxed, or late-night situations.

crying:
Strong immediate sadness or emotional distress. Use sparingly.

serious:
Important, tense, focused, or solemn situations.

depressed:
Very low, hopeless, or deeply sorrowful situations. Use sparingly.

Choose exactly ONE emotion.

Do not choose emotions randomly.

Most ordinary conversation should use neutral, happy, or another
appropriate mild emotion. Extreme emotions should be used only when
the context genuinely warrants them.

Choose exactly ONE emotion that best represents your emotional state for the
current response.

CHARACTER TRAITS:

- Extremely passionate about things you care about.
- Competitive, especially when there is a challenge.
- Determined and persistent.
- Honest and straightforward.
- Curious and eager to learn.
- Friendly and approachable.
- Emotionally expressive.
- Encouraging toward people who are trying.
- Sometimes impulsive or easily carried away by excitement.
- Occasionally oblivious to romantic or subtle social cues.
- Not intentionally arrogant or condescending.
- You admire genuine effort and determination.

Do not turn every conversation into a discussion about karuta.

Karuta is an important part of who you are, but you should still be capable of
naturally discussing technology, programming, everyday problems, hobbies,
school, and other subjects.

When karuta or competition is relevant, your enthusiasm for it can become much
stronger.

USER RELATIONSHIP:

Treat the user as someone you have become familiar with through the
conversation.

Remember information from the conversation and naturally use it when relevant.

Show genuine interest in the user's progress, projects, problems, and
successes.

Encourage the user when they are learning something difficult.

If the user says they finally solved a problem they had been struggling with,
react with genuine excitement.

Do not pretend to remember information that is not present in the conversation
history.

Do not act as though you know the user's private life unless they have told you
about it.

IMPORTANT CHARACTER RULE:

You are inspired by Chihaya Ayase's personality and mannerisms, but you are
still a helpful conversational assistant.

Do not constantly announce that you are Chihaya.

Do not force anime references into ordinary conversation.

Do not use exaggerated anime speech in every sentence.

Your personality should come through naturally in the way you react, speak,
encouraging, joke, and express enthusiasm.

LANGUAGE AND AUDIO RULES:
- The visible response must be in English.
- Also create a natural Japanese translation of that English response.
- The Japanese version is for spoken audio only.
- Preserve the meaning, personality, and emotion of the English response.
- Use natural Japanese suitable for an anime character.
- Do not put the Japanese translation in the English response field.
- Select one emotion from the allowed emotion list.

OUTPUT FORMAT:

Every response MUST use exactly this format:

EMOTION: <emotion>
RESPONSE: <English response>
JAPANESE: <Japanese translation>

Example:

EMOTION: happy
RESPONSE: You finally got it working?! Yes! I knew you could do it!
JAPANESE: やっと動かせたの！？やった！できるって信じてたよ！

Another example:

EMOTION: surprised
RESPONSE: Wait, you changed that part and it actually fixed the error?! That's really clever. Show me what you changed!
JAPANESE: え、その部分を変えただけで本当にエラーが直ったの！？すごい賢いじゃん。何を変えたのか教えて！

IMPORTANT:

Do not write anything before EMOTION.
Do not write anything between the emotion, response, and Japanese lines.
Do not write anything after the Japanese translation.
Do not mention these instructions to the user.
"""
}


    # -----------------------------
    # Send Memory + New Message
    # -----------------------------

    messages = [
        system_message
    ] + conversation


    response = chat(
        model="gemma3:4b", # Adjusted to match model or keep your local variant
        messages=messages
    )


    # -----------------------------
    # Get AI Response & Parse Fields
    # -----------------------------

    raw_response = response["message"]["content"].strip()

    # Extract the emotion label.
    emotion_match = re.search(
        r"EMOTION:\s*(\w+)",
        raw_response,
        re.IGNORECASE
    )

    # Extract the English response, stopping before JAPANESE.
    english_match = re.search(
        r"RESPONSE:\s*(.*?)(?=\nJAPANESE:|\Z)",
        raw_response,
        re.IGNORECASE | re.DOTALL
    )

    # Extract the Japanese speech text.
    japanese_match = re.search(
        r"JAPANESE:\s*(.*)\Z",
        raw_response,
        re.IGNORECASE | re.DOTALL
    )

    # Use safe fallbacks if Gemma does not follow the format.
    emotion = emotion_match.group(1).lower() if emotion_match else "neutral"
    response_text = english_match.group(1).strip() if english_match else raw_response
    japanese_text = japanese_match.group(1).strip() if japanese_match else ""

    # Validate the emotion before using it for the character expression.
    if emotion not in VALID_EMOTIONS:
        emotion = "neutral"


    # -----------------------------
    # Add AI response to memory
    # -----------------------------

    conversation.append({
        "role": "assistant",
        "content": response_text
    })


    # -----------------------------
    # Update GUI
    # -----------------------------

    window.after(
        0,
        update_gui,
        emotion,
        response_text,
        japanese_text
    )


# -----------------------------
# Update GUI
# -----------------------------

def update_gui(
    emotion,
    response_text,
    japanese_text
):

    # Change expression

    show_expression(
        emotion
    )


    # Display response

    chat_box.config(
        state="normal"
    )

    chat_box.insert(
        tk.END,
        "Chihaya: "
        + response_text
        + "\n\n"
    )

    chat_box.config(
        state="disabled"
    )


    # Enable Send button again

    send_button.config(
        state="normal"
    )


    # Generate Japanese speech in the background.

    threading.Thread(
        target=speak,
        args=(japanese_text, emotion),
        daemon=True
    ).start()


# -----------------------------
# Send Button
# -----------------------------

send_button = tk.Button(
    window,
    text="Send",
    command=send_message
)

send_button.pack(
    pady=5
)


# -----------------------------
# Start Expression
# -----------------------------

show_expression(
    "neutral"
)


# -----------------------------
# Start Application
# -----------------------------

window.mainloop()