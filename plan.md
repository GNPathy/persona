# Project Plan and Approach: Persona

This document outlines the phased implementation plan for the "Persona" project. The objective is to build a local AI system capable of mimicking a specific individual's voice, writing style, and knowledge base.

## Phase 1: Data Preparation (The Foundation)
*Critical path: High-quality data curation is required for accurate cloning.*

### 1.1 Text Corpus Generation
*   **Objective**: Create a sanitized "thought stream" text dataset.
*   **Methodology**:
    *   Ingest raw email archives (`.eml`, `.msg`) and document repositories (`.pdf`, `.docx`).
    *   Develop extraction scripts to remove non-narrative artifacts (signatures, legal disclaimers, forward chains, metadata).
    *   Consolidate cleaned text into a `corpus.txt` file for use in RAG indexing and optional fine-tuning.

### 1.2 Audio Dataset Curation
*   **Objective**: Isolate high-fidelity voice samples for synthesis.
*   **Challenge**: Existing recordings are conversational and contain overlapping speakers.
*   **Methodology**:
    *   **Manual Selection (Preferred)**: Extract 15-20 clean segments (10-30 seconds each) containing *only* the target persona's voice using audio editing tools (e.g., Audacity).
    *   **Automated Diarization (Alternative)**: Utilize speaker separation models (e.g., `pyannote-audio`, Ultimate Vocal Remover) to isolate the target track.
    *   **Requirement**: Samples must capture the full range of inflection and linguistic nuances (e.g., English/Tamil code-switching).

## Phase 2: The Brain (Model & Intelligence)
### 2.1 Core Infrastructure
*   **Action**: Deploy a local Large Language Model (LLM) optimized for consumer hardware (NVIDIA RTX 40xx).
*   **Selection**: Llama 3 (8B) or Mistral (7B) running via quantized runners (e.g., `llama-cpp-python`) for low-latency inference.

### 2.2 Knowledge Integration (RAG)
*   **Objective**: Enable factual recall and contextual grounding.
*   **Implementation**:
    *   Vectorize the `corpus.txt` from Phase 1.1 using compatible embedding models.
    *   Store vectors in ChromaDB.
    *   Construct a Retrieval Augmented Generation (RAG) pipeline to inject relevant historical context into every query.

### 2.3 Style Adaptation (Fine-Tuning)
*   **Status**: *Conditional / Secondary Step*
*   **Objective**: Capture specific linguistic idiosyncrasies and "vibe" beyond factual content.
*   **Implementation**:
    *   If RAG retrieval yields insufficient stylistic mimicry, perform Parameter-Efficient Fine-Tuning (PEFT/LoRA) using the text corpus.

## Phase 3: The Voice (TTS Engine)
### 3.1 Voice Cloning
*   **Engine**: Coqui XTTS v2 (Support for multilingual and zero-shot cloning).
*   **Implementation**:
    *   Generate speaker embeddings using the curated audio dataset from Phase 1.2.
    *   Validate synthesis quality against ground-truth recordings.

## Phase 4: Integration
### 4.1 System Orchestration
*   **Backend**: Develop a FastAPI service to handle the full interaction loop:
    1.  Receive Audio/Text Input.
    2.  Retrieve Context (RAG).
    3.  Generate Response (LLM).
    4.  Synthesize Speech (TTS).
*   **Frontend**: Develop a Progressive Web App (PWA) command interface for mobile and desktop access.
