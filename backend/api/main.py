from fastapi import FastAPI

app = FastAPI(title="Persona API")

@app.get("/")
def read_root():
    return {"message": "Persona Brain is Online"}

@app.post("/interact")
def interact(text: str):
    # TODO: Implement RAG -> LLM -> TTS pipeline
    return {"response": "This is a placeholder response.", "audio_url": None}
