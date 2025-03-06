# mAIordom

## Overview

mAIordom is designed to assist you in generating quick and full answers based on content.  
It supports various input methods such as clipboard copying, screenshot capturing, and direct recording from a microphone.  
Additionally, it supports **local LLM inference** using **Ollama**, allowing users to run models like **Qwen2.5-Coder** efficiently on their machines.

## Features

- **Clipboard Copying**: Allows users to copy text from the clipboard and update the transcription area.
- **Screenshot Capturing**: Enables users to capture text around the mouse cursor and update the transcription area.
- **Audio Recording**: Users can record audio using their microphone and transcribe it into text.
- **Quick Answer Generation**: Provides quick answers based on the transcribed text.
- **Full Answer Generation**: Generates more detailed answers based on the transcribed text.
- **Local LLM Support** (via **Ollama**): Run LLMs like **Qwen2.5-Coder** locally for privacy and performance.

## Setup

1. **Install Dependencies**:
   - Ensure you have Python >= 3.12 installed.
   - Recommended: use a virtual env
    ```sh
    python -m venv .venv
    ```
   - Setup and install required libraries:
   ```sh
    make setup
    ```

2. Install Tesseract OCR
    Download and install Tesseract OCR from:
    https://github.com/UB-Mannheim/tesseract/wiki
    Download the suitable version for your OS.

3. **Install Ollama (for Local LLM Models)**
    Download and install Ollama from https://ollama.ai.

4. **Download a Local Language Model (Recommended: Qwen2.5-Coder)**

    ```sh
     ollama pull qwen2.5-coder:3b
    ```

5. **Run the Application**:
   - Navigate to the project directory and run the application:
     make run


## Usage

### Main Window Layout

The application window is divided into several sections:

- **Close Button**: Closes the application.
- **Transcription Area** (-TRANSCRIBED_TEXT-): Displays the transcribed text.
- **Quick Answer Area** (-QUICK_ANSWER-): Shows quick answers generated based on the transcription.
- **Full Answer Area** (-FULL_ANSWER-): Displays more detailed answers.
- **Instructions**: Provides instructions for using the application.
- **Character Input** (-CHARACTER_INPUT-): Allows users to enter a custom character for the AI.
- **Model Selection** (-MODEL_COMBO-): Lets users choose the model to use.

### Key Bindings and Events

- **Clipboard Copying**:
  - Hotkeys: c, C
  - Action: Copies text from the clipboard into the transcription area and starts generating answers.
  
- **Screenshot Capturing**:
  - Hotkey: p
  - Action: Captures text around the mouse cursor and updates the transcription area, then starts generating answers.

- **Recording Audio**:
  - Hotkeys: R, A
  - Action: Starts or stops recording audio. When recording is stopped, transcribes the audio into text and generates quick/full answers.
  