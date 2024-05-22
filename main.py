from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import io
from google.oauth2 import service_account
from google.cloud import speech

app = FastAPI()

# Set up Google Cloud Speech client
client_file = 'Reksismul IAM Admin.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

@app.get("/")
async def root():
    return {"message": "Welcome to Didik!"}

@app.post("/transcribe/")
async def transcribe_audio(audio: UploadFile = File(...)):
    # Get the audio content from the request
    audio_content = await audio.read()

    # Configure the recognition settings
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='id-ID'
    )

    # Perform the transcription
    response = client.recognize(config=config, audio=audio)

    # Extract the transcript from the response
    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript + " "

    return JSONResponse(content={'transcription': transcription.strip()})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
