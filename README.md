# Persona Project: System Architecture & Implementation Cookbook

This manual provides a "recipe" for building your **Persona** application, capable of mimicking a specific individual's style and voice.

## 1. System Overview
**Goal**: Create an AI clone running locally on an NVIDIA 40xx GPU.
**Core Function**: User asks a question -> AI references emails/docs (Style/Knowledge) -> AI generates text -> AI speaks text in Persona's voice.

## 2. Hardware & Software Stack
*   **Hardware**:
    *   **GPU**: NVIDIA RTX 40xx (Recommended: 4090 for fast RAG+LLM+TTS overlapping, but 4070/4080 works well).
    *   **RAM**: 32GB+ System RAM.
*   **Software**:
    *   **OS**: Windows + WSL2 (Ubuntu) or Native Linux.
    *   **Backend**: Python 3.10+, FastAPI.
    *   **LLM (The Brain)**: [Llama 3 8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) or [Mistral 7B](https://mistral.ai/) (Optimized with GGUF/EXL2).
    *   **RAG (The Memory)**: [ChromaDB](https://www.trychroma.com/) (Vector Store) + `sentence-transformers`.
    *   **TTS (The Voice)**: [Coqui XTTS v2](https://github.com/coqui-ai/TTS) (Best for cloning from short samples).
    *   **Frontend**: React / Next.js.

## 3. Architecture Design
```mermaid
graph TD
    User[User (Web/Mobile)] -->|Question (Audio/Text)| API[FastAPI Backend]
    
    subgraph "AI PC (Backend)"
        API -->|1. Search| RAG[RAG Engine]
        RAG -->|Retrieve| VectorDB[(Emails/Docs)]
        VectorDB -->|Context| RAG
        
        RAG -->|2. Prompt (+Context)| LLM[LLM (Llama 3)]
        LLM -->|3. Text Response| API
        
        LLM -->|Text| TTS[TTS Engine (XTTS v2)]
        TTS -->|Reference Audio| AudioStore[(Voice Samples)]
        TTS -->|4. Audio Response| API
    end
    
    API -->|Audio + Text| User
```

## 4. Implementation Cookbook

### Phase 1: The Voice & Mind (Audio Only)

#### Step 1: The "Mind" (RAG & LLM)
1.  **Ingestion Script**:
    *   Parse emails (`.eml`, `.msg`) and docs (`.pdf`, `.docx`).
    *   **Cleaning**: Remove footers, legal disclaimers, and generic greetings. This is crucial for capturing the *real* style.
    *   **Chunking**: Split text into ~500 token chunks with overlap.
    *   **Embedding**: Use a model like `nomic-embed-text-v1.5` or `all-MiniLM-L6-v2` to convert chunks to vectors.
    *   **Storage**: Save to ChromaDB.
2.  **Generation Loop**:
    *   Retrieve top 3-5 relevant chunks based on user query.
    *   **System Prompt**: "You are [Name]. Answer the following question using the provided context. Mimic the writing style found in the context (e.g., brief, verbose, formal, tamil-english mix)."

#### Step 2: The "Voice" (TTS)
1.  **Data Prep**:
    *   Collect 5-10 clean audio clips (10-30 seconds each) of the persona.
    *   High quality, no background noise.
    *   *Tip*: A mix of English and Tamil samples helps capture the inflection better if using a multilingual model like XTTS-v2.
2.  **Engine**:
    *   Use **XTTS v2**. It supports voice cloning by simply passing a `.wav` file path as the speaker reference.
    *   No long training time required (Zero-shot).

#### Step 3: The API (Glue)
*   Create a simple FastAPI server.
*   Endpoint `/interact`:
    *   Input: `{"text": "What do you think about Project X?"}`
    *   Process: RAG Search -> LLM Generate -> TTS Synthesize.
    *   Output: `{"response_text": "...", "audio_url": "..."}`

#### Step 4: The Interface
*   **Web App**: Next.js.
*   **Design**: Clean, chat-like interface.
*   **Mobile**: The web app will be designed as a **PWA (Progressive Web App)**. This allows it to be installed on Android/iOS immediately without an app store.

### Phase 2: The Face (Video) - *Future Upgrade*
*   **Tool**: [SadTalker](https://github.com/OpenTalker/SadTalker) or [Wav2Lip](https://github.com/Rudrabha/Wav2Lip).
*   **Workflow**:
    *   Take the Audio generated in Phase 1.
    *   Take a static image (or video frame) of the Persona.
    *   Run the Lip-Sync model to animate the mouth to the audio.
*   *Note*: This is computationally expensive. Expect 2-5 seconds of generation time per 1 second of video on a 4090.

## 5. Next Steps
1.  **Scaffold Project**: Create the directory structure.
2.  **Environment Setup**: Install Python, CUDA, PyTorch.
3.  **Prototype**: Build a simple script to verify XTTS acts like the persona.
