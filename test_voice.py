from piper import PiperVoice
import wave


# Load the voice model
voice = PiperVoice.load("en_US-amy-medium.onnx")


# Text we want Piper to speak
text = "Hello! I'm your AI assistant. It's nice to meet you."


# Create the WAV file
with wave.open("test_voice.wav", "wb") as wav_file:

    voice.synthesize_wav(text, wav_file)


print("Voice generated successfully!")
print("Saved as test_voice.wav")