from kokoro import KPipeline
import soundfile as sf
import torch
import os
import tempfile
import click
from tqdm.autonotebook import tqdm
from utils import read_txt, concat_wav

device = "cuda" if torch.cuda.is_available() else "cpu"
pipelines = {lang_code: KPipeline(lang_code=lang_code, device=device) for lang_code in 'ab'}
pipelines['a'].g2p.lexicon.golds['kokoro'] = 'kˈOkəɹO'
pipelines['b'].g2p.lexicon.golds['kokoro'] = 'kˈQkəɹQ'


def audio_generation_from_transcription(transcription_path: str, voice: str = 'bm_george', speed: float = 1.0,
                                        output_path: str = 'output.wav'):
    print("Generating audio...")
    text = read_txt(transcription_path)
    pipeline = pipelines[voice[0]]
    generator = pipeline(text, voice=voice, speed=speed)
    audio_files = []
    progress_bar = tqdm(generator)
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, (gs, ps, audio) in enumerate(progress_bar):
            file_path = os.path.join(tmpdir, f"{i}.wav")
            progress_bar.set_description(f"Generating audio: {file_path}")
            audio_files.append(file_path)
            sf.write(file_path, audio, 24000)
        if not audio_files:
            raise ValueError("No audio files were generated. Please check the transcription and voice parameters.")
        concat_wav(audio_files, output_path)

@click.command()
@click.argument('transcription_file', type=click.Path(exists=True))
@click.option('--voice', 
              type=click.Choice(['bm_george', 'bm_daniel', 'bm_lewis', 'bm_fable', 'am_adam', 'af_bella', 'am_santa'], case_sensitive=False),
              default='bm_george', 
              help='Voice to use for audio generation')
@click.option('--speed', default=1.0, type=float, help='Speed of the generated audio')
@click.option('--output_path', default='output.wav', help='Path to save the generated audio file')
def main(transcription_file, voice, speed, output_path):
    audio_generation_from_transcription(transcription_file, voice, speed, output_path)


if __name__ == "__main__":
    main()
