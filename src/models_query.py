from dotenv import load_dotenv
from loguru import logger
import ollama

from src.config import DEFAULT_MODEL, DEFAULT_CHARACTER, OUTPUT_FILE_NAME

load_dotenv()

SYS_PREFIX: str = "You are "
SYS_SUFFIX: str = ". You will receive a question. It may not be complete. You need to understand the question and write an answer to it.\n"

SHORT_INSTRUCTION: str = "Concisely respond, limiting your answer to 50 words."
LONG_INSTRUCTION: str = "Before answering, take a deep breath and think one step at a time. Believe the answer in no more than 150 words. If the answer is code, show the code first"

client = None

def transcribe_audio(path_to_file: str = OUTPUT_FILE_NAME) -> str:
    """
    Transcribe audio from a file using the OpenAI Whisper API.

    Args:
        path_to_file (str, optional): Path to the audio file. Defaults to OUTPUT_FILE_NAME.

    Returns:
        str: The audio transcription.
    """

    logger.debug(f"Transcribing audio from: {path_to_file}...")

    with open(path_to_file, "rb") as audio_file:
        try:
            transcript = client.audio.transcriptions.create(
                file=(path_to_file, audio_file.read()),
                model="whisper-large-v3-turbo",
                prompt=SHORT_INSTRUCTION,
                response_format="text"
            )
        except Exception as error:
            logger.error(f"Can't transcribe audio: {error}")
            raise error

    logger.debug("Audio transcribed.")
    print("Transcription:", transcript.text)

    return transcript.text


def generate_answer(
        transcript: str,
        short_answer: bool = True,
        temperature: float = 0.7,
        model: str = DEFAULT_MODEL,
        character: str = DEFAULT_CHARACTER,
) -> str:
    """
    Generate an answer to the question using the Ollama API.

    Args:
        transcript (str): The audio transcription.
        short_answer (bool, optional): Whether to generate a short answer. Defaults to True.
        temperature (float, optional): The temperature to use. Defaults to 0.7.
        model (str, optional): The model to use. Defaults to DEFAULT_MODEL.
        character (str, optional): The character to use. Defaults to DEFAULT_CHARACTER.

    Returns:
        str: The generated answer.
    """
    # Generate system prompt
    system_prompt: str = SYS_PREFIX + character + SYS_SUFFIX
    if short_answer:
        system_prompt += SHORT_INSTRUCTION
    else:
        system_prompt += LONG_INSTRUCTION

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
            options={"temperature": temperature},
        )
    except Exception as error:
        logger.error(f"Can't generate answer: {error}")
        raise error

    return response["message"]["content"]
