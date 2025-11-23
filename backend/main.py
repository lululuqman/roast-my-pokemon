import os
import io
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from supabase import create_client, Client
from dotenv import load_dotenv
import google.generativeai as genai
from elevenlabs.client import ElevenLabs

# 1. Load Environment Variables
load_dotenv()

# 2. Initialize Services
# Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"), 
    os.getenv("SUPABASE_KEY")
)

# Gemini (The Brain)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# ElevenLabs (The Voice)
eleven = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Roast Backend is ALIVE!"}

@app.get("/roast/{pokemon_name}")
def get_roast(pokemon_name: str):
    pokemon_name = pokemon_name.lower().strip()

    # --- STEP 1: CHECK SUPABASE CACHE ---
    # We check if we have roasted this pokemon before to save money.
    response = supabase.table("pokemon_roasts").select("*").eq("name", pokemon_name).execute()
    
    if response.data:
        print(f"✅ Found {pokemon_name} in database. Serving cached roast.")
        return response.data[0]

    # --- STEP 2: GENERATE NEW ROAST (If not found) ---
    print(f"🔥 Generating new roast for {pokemon_name}...")
    
    try:
        # A. Generate Text with Gemini
        prompt = f"Write a short, mean, funny, and snarky roast about the Pokemon '{pokemon_name}'. Keep it under 30 words. Don't be too offensive, just funny."
        ai_response = model.generate_content(prompt)
        roast_text = ai_response.text.strip()
        print(f"📝 Text generated: {roast_text}")

        # B. Generate Audio with ElevenLabs
        # Voice ID "JBFqnCBsd6RMkjVDRZzb" is 'George' (good generic voice), change as needed
        audio_generator = eleven.text_to_speech.convert(
            text=roast_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb", 
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        # Consume the generator to get raw bytes
        audio_bytes = b"".join(audio_generator)

        # --- STEP 3: UPLOAD & SAVE ---
        
        # A. Upload MP3 to Supabase Storage
        file_path = f"{pokemon_name}.mp3"
        supabase.storage.from_("roasts").upload(
            path=file_path,
            file=audio_bytes,
            file_options={"content-type": "audio/mpeg"}
        )
        
        # B. Get the Public URL
        public_url = supabase.storage.from_("roasts").get_public_url(file_path)

        # C. Save Metadata to Database Table
        new_entry = {
            "name": pokemon_name,
            "roast_text": roast_text,
            "audio_url": public_url
        }
        supabase.table("pokemon_roasts").insert(new_entry).execute()
        
        return new_entry

    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))