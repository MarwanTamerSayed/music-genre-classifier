from fastapi import FastAPI ,File , UploadFile
import pandas as pd
import numpy as np
from tensorflow import keras
import tensorflow as tf
import librosa
import joblib
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from fastapi.responses import JSONResponse
app = FastAPI()


app.mount("/static", StaticFiles(directory="D:/Audio_Classification_Project/static"), name="static")

model = keras.models.load_model("D:/Audio_Classification_Project/model/audio_genre_model.keras")

scaler = joblib.load("D:/Audio_Classification_Project/model/music_genres_encoder.pkl")

def extract_features_from_chunks(file_path, sr=22050, chunk_duration=3):
    y, sr = librosa.load(file_path, sr=sr)  # resample to fixed rate
    samples_per_chunk = sr * chunk_duration
    total_chunks = len(y) // samples_per_chunk

    chunk_features = []

    for i in range(total_chunks):
        start = i * samples_per_chunk
        end = start + samples_per_chunk
        y_chunk = y[start:end]

        # --- MFCCs ---
        mfcc = librosa.feature.mfcc(y=y_chunk, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)

        # --- Chroma ---
        chroma = librosa.feature.chroma_stft(y=y_chunk, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        chroma_std = np.std(chroma, axis=1)

        # --- Spectral Contrast ---
        spec_contrast = librosa.feature.spectral_contrast(y=y_chunk, sr=sr)
        spec_contrast_mean = np.mean(spec_contrast, axis=1)
        spec_contrast_std = np.std(spec_contrast, axis=1)

        # --- Tempo ---
        tempo, _ = librosa.beat.beat_track(y=y_chunk, sr=sr)
        tempo = float(tempo)

        # Combine
        vector_features = np.hstack([
            mfcc_mean, mfcc_std,
            chroma_mean, chroma_std,
            spec_contrast_mean, spec_contrast_std,
            [tempo]
        ])

        chunk_features.append(vector_features)

    return chunk_features

Map = {0:'Blues',1:'Classical',2:'Country',3:'Disco',
       4:'Hiphop',5:'Jazz',6:'Metal',7:'Pop',
       8:'Reggae',9:'Rock'}

@app.get("/", response_class=HTMLResponse)
def index():
    with open("D:/Audio_Classification_Project/templates/index.html",encoding="utf-8") as f:
        return f.read()

   


@app.post('/predict')
async def predict(file:UploadFile =File(...)):
    contents = await file.read()

    with open('tmp.wav',"wb") as f:
        f.write(contents)

    tmp = extract_features_from_chunks("tmp.wav")
    tmp_scaled = scaler.transform(tmp)   
    preds = model.predict(np.array(tmp_scaled))   
    preds_classes = np.argmax(preds, axis=1)    
    final_class = np.bincount(preds_classes).argmax()
    return JSONResponse({"genre": Map[final_class]})