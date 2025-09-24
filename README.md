# 🎵 Music Genre Classifier

A web application that classifies the genre of a music file using an Artificial Neural Network (ANN) and provides a **modern, interactive frontend** for users to upload and listen to their songs.

---

## **Project Overview**

This project performs the following steps:

1. **Data Exploration & Visualization**  
   - Plotted sample audio files for each genre.  
   - Visualized spectrograms to observe differences between genres.

2. **Feature Extraction**  
   - Implemented a function to split audio into **chunks**.  
   - Extracted features from each chunk, including:  
     - MFCCs  
     - Chroma  
     - Spectral contrast  
     - Tempo  

3. **Model Training**  
   - Preprocessed the extracted features.  
   - Trained an **Artificial Neural Network (ANN)** on the processed dataset.  
   - Achieved **~90% accuracy** in classifying music genres.

4. **Model Deployment**  
   - Deployed the trained model using **FastAPI**.  
   - Users can **upload audio files** and receive predicted genres.  

5. **Frontend**  
   - A **one-page modern interface** with a cool equalizer-style loader.  
   - Users can **preview the uploaded audio** while waiting for predictions.  
   - Responsive and visually appealing design.

---

## **Technologies Used**

- **Python:** NumPy, Pandas, Librosa, TensorFlow/Keras, Joblib  
- **Machine Learning:** Artificial Neural Networks (ANN)  
- **Web Framework:** FastAPI  
- **Frontend:** HTML, CSS, JavaScript  
- **Visualization:** Matplotlib, Seaborn  

---

