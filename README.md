# one-object-loom
## A single-branch auto-itterating text generator using phi3:mini and ollama
Inspired by slimepriestess telling us about [Command Loom Interface](https://github.com/socketteer/clooi), this project implements a single-branch auto-itterative text generator in Python3.
## Requirements:
* [Ollama](https://ollama.com/) installed
   * The python bindings for ollama (`pip3 install ollama`) installed.


     ## Usage
     Clone this repository and  then do
     ```
     ollama create loomphi
     python ool.py
     ```
This will create the LoomPhi model, a modified version of Microsoft's Phi3:mini model with an adjusted temperature that is better suited to xenogenetic text generation

## Credits go to:
* Slimepriestess - for the initial idea of looms, as well as the song lyrics that comprise the initial uer message
* Rozaya (CommunityBelonging) for contributions regarding the "continuation phrase feature"
  
