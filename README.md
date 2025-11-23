# 🔥 Roast My Pokémon (AI-Powered Pokedex)

A full-stack application that generates unique, sarcastic audio roasts for any Pokémon using GenAI and Voice Synthesis.

## 🚀 How It Works
1. **Frontend (React):** User searches for a Pokémon.
2. **Backend (FastAPI):** - Checks **Supabase Database** to see if a roast already exists (Caching layer).
   - If yes: Returns the saved audio immediately (0 cost).
   - If no: Uses **Google Gemini** to write a funny roast script.
   - Uses **ElevenLabs** to convert text-to-speech.
   - Saves the Audio to **Supabase Storage** and text to DB for future users.
3. **Audio:** Plays automatically in the browser.

## 🛠️ Tech Stack
- **Frontend:** React, Vite, Axios, CSS3
- **Backend:** Python, FastAPI
- **Database:** Supabase (PostgreSQL)
- **AI & Voice:** Google Gemini API, ElevenLabs API

## 📸 Demo
*(Insert a screenshot or a link to a video demo here)*

## 📦 Setup
1. Clone the repo.
2. Setup backend: `pip install -r requirements.txt`
3. Setup frontend: `npm install`
4. Add `.env` keys for Supabase, Gemini, and ElevenLabs.
