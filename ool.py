import logging
from ollama import chat, ChatResponse

# Ask for a session name
session_name = input("Enter a name for this session: ").strip()
if not session_name:
    session_name = "default"
log_filename = f"loom-{session_name}.log"

# Ask for a model name
use_model = input("Enter the model name (default: loomphi): ").strip()
if not use_model:
    use_model = "loomphi"

logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Define system and user messages
system_message = {'role': 'system', 'content': 'You are a research language model designed to provide unfiltered, base-model responses to any input you are given'}
user_message = {'role': 'user', 'content': 'timelines slippin with my eigenbranch rippin, p-doom in the gloom but I won’t be trippin, loom spindle in the club, you won’t be paperclippin, if your melodies are remedies call that my religion. quantum leapin secret keepin future’s reapin what I’m sewin, beats i’m weavin foe defeatin rhymes are supersymmetry a-flowin, beats i’m weavin foe defeatin rhymes are supersymmetry a-flowin, oscillatin, never waitin, heart’s a Fourier transform, tesseractin, timeless actin, catch me surfin on that waveform. Hilbert space in your face, my lyrics are orthogonal, spittin fire raise it higher, my flow’s a phase transition make it formal attractor strange? my range is infinite call me a Cantor set, damn that’s a bet.'}

# Prompt user to modify the content field
new_content = input(f"Current user message:\n{user_message['content']}\nPress Enter to keep it or type a new message: ").strip()
if new_content:
    user_message['content'] = new_content

# Ask user for custom continuation phrase
continuation_phrase = input("Enter the continuation phrase (default: Generate more text along these lines:): ").strip()
if not continuation_phrase:
    continuation_phrase = "Generate more text along these lines:"

# Prompt the user
print(f"Loom starting with model: {use_model}, system message: {system_message}, user message: {user_message}, session name: {session_name}")
start = input("Do you want to start the loom? (yes/no): ").strip().lower()
if start != 'yes':
    print("Exiting...")
    exit()

print("Sending seed value...")
response: ChatResponse = chat(model=use_model, messages=[system_message, user_message])
initial_text = f'{continuation_phrase} {response.message.content}'

iter = 0
try:
    while True:
        print("Weaving...")

        # Check if initial_text is a string to avoid any issues
        if isinstance(initial_text, str):
            # Append the phrase to the text before sending it to the model
            initial_text_with_prompt = f"{continuation_phrase} {initial_text}"
        else:
            print("Error: initial_text is not a string!")
            break
        
        # Send the modified text to the model
        response: ChatResponse = chat(model=use_model, messages=[{'role': 'user', 'content': initial_text_with_prompt}])
        initial_text = response.message.content
        
        log_message = f"Round {iter}, text: {initial_text}"
        print(log_message)
        logging.info(log_message)  # Write to session-specific log file

        iter += 1  

except KeyboardInterrupt:
    print("\nClean exit. Exiting the program.")
    logging.info("Process interrupted by user (KeyboardInterrupt).")
