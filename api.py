from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import tempfile
import uuid
from main import audio_generation_from_transcription

app = FastAPI(title="Text-to-Speech API", description="API for generating audio from text using Kokoro TTS")

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = 'bm_george'
    speed: Optional[float] = 1.0
    
class TTSResponse(BaseModel):
    message: str
    audio_file_id: str
    download_url: str

# Dictionary to store generated audio files temporarily
generated_files = {}
@app.post("/generate-audio")
async def generate_audio(
    file: UploadFile = File(..., description="Upload a text file for audio generation"),
    voice: str = 'bm_george',
    speed: float = 1.0
):
    """
    Generate audio from uploaded text file
    """
    valid_voices = ['bm_george', 'bm_daniel', 'bm_lewis', 'bm_fable', 'am_adam', 'af_bella', 'am_santa']
    if voice not in valid_voices:
        raise HTTPException(status_code=400, detail=f"Invalid voice. Must be one of: {valid_voices}")

    if speed <= 0:
        raise HTTPException(status_code=400, detail="Speed must be greater than 0")

    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="File must be a .txt file")
    
    try:
        file_id = str(uuid.uuid4())

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as temp_input:
            content = await file.read()
            temp_input.write(content)
            temp_input_path = temp_input.name

        output_filename = f"{file_id}.wav"
        output_path = os.path.join(tempfile.gettempdir(), output_filename)
        
        # Generate audio
        audio_generation_from_transcription(
            transcription_path=temp_input_path,
            voice=voice,
            speed=speed,
            output_path=output_path
        )

        generated_files[file_id] = {
            'file_path': output_path,
            'filename': output_filename
        }

        os.unlink(temp_input_path)
        
        return TTSResponse(
            message="Audio generated successfully from uploaded file",
            audio_file_id=file_id,
            download_url=f"/download/{file_id}"
        )
        
    except Exception as e:
        # Clean up temp files on error
        if 'temp_input_path' in locals() and os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if 'output_path' in locals() and os.path.exists(output_path):
            os.unlink(output_path)
        
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")

@app.get("/download/{file_id}")
async def download_audio(file_id: str):
    """
    Download generated audio file
    """
    if file_id not in generated_files:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    file_info = generated_files[file_id]
    file_path = file_info['file_path']
    filename = file_info['filename']
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='audio/wav'
    )

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Text-to-Speech API using Kokoro TTS",
        "endpoints": {
            "POST /generate-audio": "Generate audio from uploaded text file",
            "GET /download/{file_id}": "Download generated audio file",
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
