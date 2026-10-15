
# Import the built-in modules needed for the local speech server.
import json
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

# Import XTTS from your existing Coqui TTS installation.
from TTS.api import TTS

# Find the main project folder from this script's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Store reference recordings inside the main project.
REFERENCE_DIR = PROJECT_ROOT / "assets" / "voice_references"

# Store generated speech in the project's output folder.
OUTPUT_DIR = PROJECT_ROOT / "output" / "audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Map the AI's emotions to your reference audio recordings.
VOICE_REFERENCES = {
    "sad": REFERENCE_DIR / "Lucy_Nostalgic_Sad.wav",
    "crying": REFERENCE_DIR / "Lucy_Nostalgic_Sad.wav",
    "depressed": REFERENCE_DIR / "Lucy_Nostalgic_Sad.wav",
    "worried": REFERENCE_DIR / "Lucy_Nostalgic_Sad.wav",

    "happy": REFERENCE_DIR / "Lucy_Upbeat_Curious_PLayful.wav",
    "excited": REFERENCE_DIR / "Lucy_Upbeat_Curious_PLayful.wav",
    "surprised": REFERENCE_DIR / "Lucy_Upbeat_Curious_PLayful.wav",
    "embarrassed": REFERENCE_DIR / "Playful_Laughing.wav",

    "neutral": REFERENCE_DIR / "Lucy_Upbeat_Curious_PLayful.wav",
}

# Use the neutral reference for unmapped emotions.
DEFAULT_REFERENCE = VOICE_REFERENCES["neutral"]

# Prevent simultaneous requests from using the GPU model at the same time.
generation_lock = threading.Lock()

# Load XTTS once when the server starts, rather than once per reply.
print("Loading XTTS-v2 onto the GPU. The first startup may take a while...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")
print("XTTS-v2 is ready to generate speech.")

# Define the local HTTP API.
class SpeechHandler(BaseHTTPRequestHandler):

    # Process requests to generate Japanese speech.
    def do_POST(self):
        # Only accept requests at the speech-generation endpoint.
        if urlparse(self.path).path != "/speak":
            self.send_error(404, "Unknown endpoint")
            return

        try:
            # Read the JSON request body.
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length <= 0 or content_length > 100_000:
                self.send_error(400, "Invalid request size")
                return

            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))

            # Read the Japanese text and emotion supplied by the assistant.
            japanese_text = str(data.get("text", "")).strip()
            emotion = str(data.get("emotion", "neutral")).lower()

            # Reject empty speech and overly long requests.
            if not japanese_text:
                self.send_error(400, "Speech text cannot be empty")
                return
            if len(japanese_text) > 2000:
                self.send_error(400, "Speech text is too long")
                return

            # Select the appropriate reference recording.
            reference_wav = VOICE_REFERENCES.get(
                emotion, DEFAULT_REFERENCE
            )

            # Confirm that the voice sample exists.
            if not reference_wav.is_file():
                self.send_error(500, "Voice reference file is missing")
                return

            # Give every response its own audio file to avoid overwrites.
            output_file = OUTPUT_DIR / f"speech_{uuid.uuid4().hex}.wav"

            # Generate audio using the already-loaded XTTS model.
            with generation_lock:
                tts.tts_to_file(
                    text=japanese_text,
                    speaker_wav=str(reference_wav),
                    language="ja",
                    file_path=str(output_file),
                )

            # Return the generated audio path to the assistant.
            result = json.dumps({
                "audio_path": str(output_file)
            }).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(result)))
            self.end_headers()
            self.wfile.write(result)

            print(f"Generated {output_file.name} using emotion: {emotion}")

        except Exception as error:
            # Log the real error in the server terminal.
            print(f"Speech generation error: {error}")

            # Send a generic error message to the assistant.
            message = json.dumps({
                "error": "Japanese speech generation failed"
            }).encode("utf-8")

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(message)))
            self.end_headers()
            self.wfile.write(message)

    # Keep normal HTTP request logging available for debugging.
    def log_message(self, format, *args):
        print("TTS server:", format % args)


# Listen only on this computer; the API is not exposed to your network.
server = ThreadingHTTPServer(("127.0.0.1", 8765), SpeechHandler)

print("TTS server listening at http://127.0.0.1:8765")
print("Keep this terminal open while using the assistant.")

# Continue serving requests until the server is stopped.
server.serve_forever()
