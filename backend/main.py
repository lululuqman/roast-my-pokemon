from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow React to talk to Python (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development only
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Roast Backend is ALIVE!"}