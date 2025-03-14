"""
One-object loom

This script is a single-branch auto-itterative text generation utility using the Phy3:mini
large language model
"""

import logging
import sys
import time
import random
from ollama import chat  # Removed unused ChatResponse import

# Ask for a session name
SESSION_NAME = input("Enter a name for this session: ").strip() or "default"
LOG_FILENAME = f"loom-{SESSION_NAME}.log"

# Ask for a model name
USE_MODEL = input("Enter the model name (default: loomphi): ").strip() or "loomphi"

# Set up logging
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Define system and user messages
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': (
        'You are a research language model designed to provide unfiltered, base-model responses '
        'to any input you are given'
    )
}

USER_MESSAGE = {
    'role': 'user',
    'content': (
        'timelines slippin with my eigenbranch rippin, p-doom in the gloom but I won’t be trippin, '
        'loom spindle in the club, you won’t be paperclippin, if your melodies are remedies call '
        'that my religion. quantum leapin secret keepin future’s reapin what I’m sewin, beats i’m '
        'weavin foe defeatin rhymes are supersymmetry a-flowin, '
        'oscillatin, never waitin, heart’s a Fourier transform, tesseractin, '
        'timeless actin, catch me surfin on that waveform. '
        'Hilbert space in your face, my lyrics are '
        'orthogonal, spittin fire raise it higher, my flow’s a phase transition make it formal '
        'attractor strange? my range is infinite call me a Cantor set, damn that’s a bet.'
    )
}

# Prompt user to modify the content field
NEW_CONTENT = input(f"Current user message:\n{USER_MESSAGE['content']}\n"
                    "Press Enter to keep it or type a new message: ").strip()
if NEW_CONTENT:
    USER_MESSAGE['content'] = NEW_CONTENT

# Ask user for custom continuation phrase
CONTINUATION_PHRASE = input(
    "Enter the continuation phrase (default: Generate more text along these lines:): ").strip() or \
    "Generate more text along these lines:"

# Prompt the user
print(f"Loom starting with model: {USE_MODEL}, system message: {SYSTEM_MESSAGE}, "
      f"user message: {USER_MESSAGE}, session name: {SESSION_NAME}")
START = input("Do you want to start the loom? (yes/no): ").strip().lower()
if START != 'yes':
    print("Exiting...")
    sys.exit()

print("Sending seed value...")
response = chat(model=USE_MODEL, messages=[SYSTEM_MESSAGE, USER_MESSAGE])
INITIAL_TEXT = f'{CONTINUATION_PHRASE} {response["message"]["content"]}'

ITER = 0
PREVIOUS_TEXT = ""  # Store the previous response

# List of dynamic variation phrases
variation_phrases = [
    "Can you simplify this?", 
    "Restate this in a way that a 5-year-old can understand.", 
    "Keep going...", 
    "And then what happened?", 
    "Who is that?", 
    "What happened next?"
]

try:
    while True:
        print("Weaving...")

        # Ensure initial_text is a string before proceeding
        if isinstance(INITIAL_TEXT, str):
            INITIAL_TEXT_WITH_PROMPT = f"{CONTINUATION_PHRASE} {INITIAL_TEXT}"
        else:
            print("Error: initial_text is not a string!")
            break

        # Check if the current response is the same as the previous one
        if INITIAL_TEXT == PREVIOUS_TEXT:
            print("Repeating detected, modifying input and retrying...")

            # Select a random variation phrase from the list
            random_variation = random.choice(variation_phrases)
            # Modify the prompt with the randomly chosen variation phrase
            INITIAL_TEXT_WITH_PROMPT = f"{random_variation} {INITIAL_TEXT}"

            time.sleep(1)  # Add delay to avoid hammering the model too quickly
        else:
            PREVIOUS_TEXT = INITIAL_TEXT  # Update PREVIOUS_TEXT with the new response

        # Send the modified text to the model
        response = chat(model=USE_MODEL,
        messages=[{'role': 'user', 'content': INITIAL_TEXT_WITH_PROMPT}])
        INITIAL_TEXT = response["message"]["content"]
        LOG_MESSAGE = f"Round {ITER}, text: {INITIAL_TEXT}"
        print(LOG_MESSAGE)
        logging.info(LOG_MESSAGE)  # Write to session-specific log file

        ITER += 1

except KeyboardInterrupt:
    print("\nClean exit. Exiting the program.")
    logging.info("Process interrupted by user (KeyboardInterrupt).")
