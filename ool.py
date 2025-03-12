"""
Loom Chat Session Logger

This script handles the setup of a chat session with a model, logs the conversation to a session-specific
log file, and allows the user to interactively modify the messages exchanged with the model.
"""

import logging
from ollama import chat, ChatResponse

# Ask for a session name
SESSION_NAME = input("Enter a name for this session: ").strip() or "default"
LOG_FILENAME = f"loom-{SESSION_NAME}.log"

# Ask for a model name
USE_MODEL = input("Enter the model name (default: loomphi): ").strip() or "loomphi"

# Set up logging
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s - %(message)s')

# Define system and user messages
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': 'You are a research language model designed to provide unfiltered, base-model responses to any input you are given'
}

USER_MESSAGE = {
    'role': 'user',
    'content': 'timelines slippin with my eigenbranch rippin, p-doom in the gloom but I won’t be trippin, loom spindle in the club, you won’t be paperclippin, if your melodies are remedies call that my religion. quantum leapin secret keepin future’s reapin what I’m sewin, beats i’m weavin foe defeatin rhymes are supersymmetry a-flowin, beats i’m weavin foe defeatin rhymes are supersymmetry a-flowin, oscillatin, never waitin, heart’s a Fourier transform, tesseractin, timeless actin, catch me surfin on that waveform. Hilbert space in your face, my lyrics are orthogonal, spittin fire raise it higher, my flow’s a phase transition make it formal attractor strange? my range is infinite call me a Cantor set, damn that’s a bet.'
}

# Prompt user to modify the content field
NEW_CONTENT = input(f"Current user message:\n{USER_MESSAGE['content']}\nPress Enter to keep it or type a new message: ").strip()
if NEW_CONTENT:
    USER_MESSAGE['content'] = NEW_CONTENT

# Ask user for custom continuation phrase
CONTINUATION_PHRASE = input("Enter the continuation phrase (default: Generate more text along these lines:): ").strip() or "Generate more text along these lines:"

# Prompt the user
print(f"Loom starting with model: {USE_MODEL}, system message: {SYSTEM_MESSAGE}, user message: {USER_MESSAGE}, session name: {SESSION_NAME}")
START = input("Do you want to start the loom? (yes/no): ").strip().lower()
if START != 'yes':
    print("Exiting...")
    exit()

print("Sending seed value...")
response: ChatResponse = chat(model=USE_MODEL, messages=[SYSTEM_MESSAGE, USER_MESSAGE])
INITIAL_TEXT = f'{CONTINUATION_PHRASE} {response.message.content}'

ITER = 0
try:
    while True:
        print("Weaving...")

        # Ensure initial_text is a string before proceeding
        if isinstance(INITIAL_TEXT, str):
            INITIAL_TEXT_WITH_PROMPT = f"{CONTINUATION_PHRASE} {INITIAL_TEXT}"
        else:
            print("Error: initial_text is not a string!")
            break
        
        # Send the modified text to the model
        response: ChatResponse = chat(model=USE_MODEL, messages=[{'role': 'user', 'content': INITIAL_TEXT_WITH_PROMPT}])
        INITIAL_TEXT = response.message.content
        
        log_message = f"Round {ITER}, text: {INITIAL_TEXT}"
        print(log_message)
        logging.info(log_message)  # Write to session-specific log file

        ITER += 1  

except KeyboardInterrupt:
    print("\nClean exit. Exiting the program.")
    logging.info("Process interrupted by user (KeyboardInterrupt).")
