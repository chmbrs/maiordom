from typing import Any, Dict

import os
import FreeSimpleGUI as sg
from loguru import logger
import pyperclip
import pyautogui
import pytesseract

from src import audio, models_query
from src.button import OFF_IMAGE, ON_IMAGE
from src.config import TESSERACT_EXE_PATH, SCREENSHOT_CAPTURE_HOTKEY

if TESSERACT_EXE_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE_PATH


def handle_events(window: sg.Window, event: str, values: Dict[str, Any]) -> None:
    """
    Handle the events. Record audio, transcribe audio, generate quick and full answers.

    Args:
        window (sg.Window): The window element.
        event (str): The event.
        values (Dict[str, Any]): The values of the window.
    """
    # If the user is not focused on the position input, process the events
    focused_element: sg.Element = window.find_element_with_focus()
    if (not focused_element or
            focused_element.Key not in ["-CHARACTER_INPUT-", "-X_SCREENSHOT_LENGTH_INPUT-", "-Y_SCREENSHOT_LENGTH_INPUT-"]):

        if event in ("r", "R", "-RECORD_BUTTON-") or "r" in event:
            recording_event(window)

        elif event in ("a", "A", "-ANALYZE_BUTTON-") or "a" in event:
            transcribe_event(window)

        elif event in ("v", "V", "-TRANSCRIBED_TEXT-") or "v" in event:
            copied_text = pyperclip.paste()
            window["-TRANSCRIBED_TEXT-"].update(copied_text)
            start_generating_answers(window, values, copied_text)

        elif event in (SCREENSHOT_CAPTURE_HOTKEY, SCREENSHOT_CAPTURE_HOTKEY.upper()) or SCREENSHOT_CAPTURE_HOTKEY in event:
            text = get_text_around_mouse(values)
            window["-TRANSCRIBED_TEXT-"].update(text)
            start_generating_answers(window, values, text)

    elif event[:6] in ("Return", "Escape"):
        window["-ANALYZE_BUTTON-"].set_focus()

    # When the transcription is ready
    elif event == "-WHISPER-":
        answer_events(window, values)

    # When the quick answer is ready
    if event == "-QUICK_ANSWER-":
        logger.debug("Quick answer generated.")
        print("Quick answer:", values["-QUICK_ANSWER-"])
        window["-QUICK_ANSWER-"].update(values["-QUICK_ANSWER-"])

    # When the full answer is ready
    if event == "-FULL_ANSWER-":
        logger.debug("Full answer generated.")
        print("Full answer:", values["-FULL_ANSWER-"])
        window["-FULL_ANSWER-"].update(values["-FULL_ANSWER-"])


def recording_event(window: sg.Window) -> None:
    """
    Handle the recording event. Record audio and update the record button.

    Args:
        window (sg.Window): The window element.
    """
    button: sg.Element = window["-RECORD_BUTTON-"]
    button.metadata.state = not button.metadata.state
    button.update(image_data=ON_IMAGE if button.metadata.state else OFF_IMAGE)

    # Record audio
    if button.metadata.state:
        window.perform_long_operation(lambda: audio.record(button), "-RECORDED-")


def transcribe_event(window: sg.Window) -> None:
    """
    Handle the transcribe event. Transcribe audio and update the text area.

    Args:
        window (sg.Window): The window element.
    """
    transcribed_text: sg.Element = window["-TRANSCRIBED_TEXT-"]
    transcribed_text.update("Transcribing audio...")

    # Transcribe audio
    window.perform_long_operation(models_query.transcribe_audio, "-WHISPER-")

def get_text_around_mouse(values: Dict[str, Any]) -> str:
    logger.debug("Screenshoting..")

    x_mouse_position, y_mouse_position = pyautogui.position()

    screenshot_x_length = values["-X_SCREENSHOT_LENGTH_INPUT-"]
    screenshot_y_length = values["-Y_SCREENSHOT_LENGTH_INPUT-"]

    screenshot = pyautogui.screenshot(region=(
        x_mouse_position - 20, y_mouse_position - 20, int(screenshot_x_length), int(screenshot_y_length)
    ))
    screenshot.save("screen.png")

    logger.debug("Getting text from screenshot...")
    extracted_text = pytesseract.image_to_string(screenshot)
    cleaned_extracted_text = os.linesep.join([s for s in extracted_text.splitlines() if s])
    logger.debug(f"Prompt: {cleaned_extracted_text}")

    return cleaned_extracted_text

def start_generating_answers(window: sg.Window, values: Dict[str, Any], prompt) -> None:
    quick_answer: sg.Element = window["-QUICK_ANSWER-"]
    full_answer: sg.Element = window["-FULL_ANSWER-"]

    # Get model and character
    model: str = values["-MODEL_COMBO-"]
    character: str = values["-CHARACTER_INPUT-"]

    # Generate quick answer
    logger.debug("Generating quick answer...")
    quick_answer.update("Generating quick answer...")
    window.perform_long_operation(
        lambda: models_query.generate_answer(
            prompt,
            short_answer=True,
            temperature=0,
            model=model,
            character=character,
        ),
        "-QUICK_ANSWER-",
    )

    # Generate full answer
    logger.debug("Generating full answer...")
    full_answer.update("Generating full answer...")
    window.perform_long_operation(
        lambda: models_query.generate_answer(
            prompt,
            short_answer=False,
            temperature=0.7,
            model=model,
            character=character,
        ),
        "-FULL_ANSWER-",
    )

def answer_events(window: sg.Window, values: Dict[str, Any]) -> None:
    transcribed_text: sg.Element = window["-TRANSCRIBED_TEXT-"]
    quick_answer: sg.Element = window["-QUICK_ANSWER-"]
    full_answer: sg.Element = window["-FULL_ANSWER-"]

    # Get audio transcript and update text area
    audio_transcript: str = values["-WHISPER-"]
    transcribed_text.update(audio_transcript)

    # Get model and character
    model: str = values["-MODEL_COMBO-"]
    character: str = values["-CHARACTER_INPUT-"]

    # Generate quick answer
    logger.debug("Generating quick answer...")
    quick_answer.update("Generating quick answer...")
    window.perform_long_operation(
        lambda: models_query.generate_answer(
            audio_transcript,
            short_answer=True,
            temperature=0,
            model=model,
            character=character,
        ),
        "-QUICK_ANSWER-",
    )

    # Generate full answer
    logger.debug("Generating full answer...")
    full_answer.update("Generating full answer...")
    window.perform_long_operation(
        lambda: models_query.generate_answer(
            audio_transcript,
            short_answer=False,
            temperature=0.7,
            model=model,
            character=character,
        ),
        "-FULL_ANSWER-",
    )
