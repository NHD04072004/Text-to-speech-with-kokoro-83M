# Text to speech with kokoro-83M

### Feature
- Convert text to audio
- Select voice (default: bm_george)
- Audio speed (default: 1.0)

### Requirements

- OS: Ubuntu 18.04+
- Python 3.11+
- Create virtual environment
```bash
# Without Astral uv
python3 -m venv <env_name>
source <env_name>/bin/activate

# With Astral uv
uv init
```
- Installing dependencies
```bash
# With pip
pip install kokoro>=0.9.4 soundfile pip tqdm
# or
pip install -r requirements.txt

# With Astral uv
uv add kokoro>=0.9.4 soundfile pip tqdm
# or
uv add -r requirements.txt  # or uv pip install -r requirements.txt
```

### Run

- Run with `python` script
```bash
# With uv
uv run main.py <transcription_file_txt> --voice <optional_voice_name> --speed <optional_speed> --output <optional_output_path>

# Without uv
python main.py <transcription_file_txt> --voice <optional_voice_name> --speed <optional_speed> --output <optional_output_path>
```
- Run with `bash`
```bash
# if chmod
bash ./run.sh <transcription_file_txt> --voice <optional_voice_name> --speed <optional_speed> --output <optional_output_path>

# else, chmod before
chmod +x ./run.sh
# then run
```
- Maybe run now by `double-click`