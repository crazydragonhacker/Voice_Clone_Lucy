# Jaru - Japanese Voice Generation

## Project status

Checkpoint: Japanese voice generation using Coqui XTTS-v2.

## Current capabilities

- Generate Japanese speech from text.
- Use a reference WAV for voice cloning.
- Run locally on Windows with Python 3.11.
- Generate WAV output.

## Requirements

- Windows 10/11
- Python 3.11
- Git
- FFmpeg shared build available on PATH
- Sufficient disk space for the XTTS-v2 model

## Setup

Create a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the recorded dependencies:

```powershell
python -m pip install -r requirements.txt
```

Ensure FFmpeg is installed and accessible:

```powershell
ffmpeg -version
```

## Voice generation

Place an authorized reference WAV in the local samples folder.

Example:

```powershell
New-Item -ItemType Directory -Force samples, output
```

Run the Japanese synthesis test:

```powershell
tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 --text "こんにちは！今日は何をしようか？" --speaker_wav "D:\JaruVoice\samples\Lucy_Upbeat_Curious_PLayful.wav" --language_idx ja --out_path "D:\JaruVoice\output\jaru_test.wav"
```

Change the reference path to match your local file.

## Current checkpoint

- XTTS-v2 model downloaded.
- FFmpeg and TorchCodec audio decoding verified.
- Japanese text processing verified using Fugashi and UniDic Lite.
- Japanese speech generation completed successfully.
- Output file: `output/jaru_test.wav` (local, not committed).

## Known limitations

- CPU inference is relatively slow.
- Voice cloning does not guarantee exact emotional reproduction.
- Dynamic assistant responses and VTuber animation integration are not implemented yet.

## Privacy and licensing

Do not commit private reference recordings, generated voice clips, model weights, API keys, or personal data.

Only clone voices you have permission to use. Review the applicable model license before commercial use.
