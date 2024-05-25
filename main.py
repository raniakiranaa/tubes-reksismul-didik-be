from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import service_account
from google.cloud import speech
from pydantic import BaseModel
from typing import List
from tasks import tasks, tasks_read2
from pydub import AudioSegment
import io
import os

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client_file = './Reksismul IAM Admin.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

class CheckRequest(BaseModel):
    taskIndex: int
    selectedWords: List[str]

user_scores = {}
user_scores_read2 = {}

@app.get("/api/tasks")
async def get_tasks():
    return JSONResponse(content=tasks)

@app.get("/api/tasks_read2")
async def get_tasks_read2():
    return JSONResponse(content=tasks_read2)

@app.post("/api/check")
async def check_words(request: CheckRequest):
    task = tasks[request.taskIndex]
    correct_words = task["correct"]
    correct_count = len([word for word in request.selectedWords if word in correct_words])
    all_correct = correct_count == len(correct_words)

    # Store the result for the user
    user_scores[request.taskIndex] = {
        "correctCount": correct_count,
        "total": len(correct_words)
    }

    return JSONResponse(content={"correctCount": correct_count, "allCorrect": all_correct})

@app.post("/api/check_read2")
async def check_words_read2(request: CheckRequest):
    task = tasks_read2[request.taskIndex]
    correct_words = task["correct"]
    correct_count = len([word for word in request.selectedWords if word in correct_words])
    all_correct = correct_count == len(correct_words)

    # Store the result for the user
    user_scores_read2[request.taskIndex] = {
        "correctCount": correct_count,
        "total": len(correct_words)
    }

    return JSONResponse(content={"correctCount": correct_count, "allCorrect": all_correct})

@app.get("/api/score")
async def get_score():
    total_correct = sum([score["correctCount"] for score in user_scores.values()])
    total_possible = sum([score["total"] for score in user_scores.values()])
    percentage = (total_correct / total_possible) * 100 if total_possible > 0 else 0
    return JSONResponse(content={"score": percentage})

@app.get("/api/score_read2")
async def get_score_read2():
    total_correct = sum([score["correctCount"] for score in user_scores_read2.values()])
    total_possible = sum([score["total"] for score in user_scores_read2.values()])
    percentage = (total_correct / total_possible) * 100 if total_possible > 0 else 0
    return JSONResponse(content={"score": percentage})

@app.post("/transcribe/")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        # Read the audio content
        audio_content = await audio_file.read()
        
        # Convert audio to correct format using pydub
        audio = AudioSegment.from_file(io.BytesIO(audio_content))
        audio = audio.set_frame_rate(48000).set_channels(1).set_sample_width(2)

        # Save the corrected audio to a BytesIO object
        corrected_audio_io = io.BytesIO()
        audio.export(corrected_audio_io, format="wav")
        corrected_audio_content = corrected_audio_io.getvalue()

        # Log the file content type and length for debugging
        print(f"File content type: {audio_file.content_type}")
        print(f"File content length: {len(corrected_audio_content)} bytes")

        # Create a RecognitionAudio instance
        recognition_audio = speech.RecognitionAudio(content=corrected_audio_content)

        # Create a RecognitionConfig instance
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=48000,  # Explicitly set the sample rate
            language_code='id-ID'
        )

        # Perform speech recognition
        response = client.recognize(config=config, audio=recognition_audio)

        # Log the full response for debugging
        print(f"API response: {response}")

        # Check if there are results in the response
        if not response.results:
            print("No transcription results found. Check audio quality and content.")
            return JSONResponse(content={'transcription': '', 'error': 'No transcription results found. Check audio quality and content.'})

        # Extract transcription from response
        transcription = " ".join(result.alternatives[0].transcript for result in response.results)

        return JSONResponse(content={'transcription': transcription})
    except Exception as e:
        print(f"An error occurred during transcription: {str(e)}")
        raise HTTPException(status_code=400, detail=f"An error occurred during transcription: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)