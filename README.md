# Tutorial: Building a Discord Bot with Local Ollama Model Integration
A guide and template for building a Discord bot that connects to locally installed AI models from Ollama using a local API. This project is perfect for developers looking to integrate AI features into their bots with local model inference.

## Requirements

- Python 3.8+
- Ollama (with models installed)
- Git
- Discord Developer Token
- discord.py library
- python-dotenv for environment variable management
- requests library to handle API calls


## Clone the repository:

```
git clone https://github.com/AnotherG0AT/Discord-Bot-with-Local-Ollama-Model-Integration.git
cd discord-bot-ollama-model-integration # and switch to the directory
```

## Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Set up the environment variables:

 ## Install dependencies:

```
pip install -r requirements.txt
```

## Make changes in the code
- Right click on the bot.py file and click edit with [whichever app you use (ex:notepad) ]
- Then go find 
```
# Your bot token
DISCORD_TOKEN = 'your discord bot token'

```
- And replace the your discord bot token with your actual discord bot token from Discord Developer Portal.
- You also have to replace
```
# Function to get response from the Ollama model
def get_ollama_response(prompt, model="your model id here"):
```
your model id here with your actual ollama model id (for example: phi3)

## How to download ollama models?

- Go to their official website: https://ollama.com/download/windows
- Download ollama and install it.
- Now open a Terminal/Command Promt and type
```
ollama pull [your model id]
```
- Then you can test the model by using
```
ollama run [your model id]
```
- You can find ollama model id's and what they do/what they are for from their library: https://ollama.com/library

## Running the Bot

Start the Ollama API: Ensure your local Ollama API is running on http://localhost:11434.

## Run the bot:
- open a terminal/cmd prompt on the directory where the repo is in and run
```
python bot.py
```
Usage
```
!ai <prompt>: Sends a prompt to the locally running Ollama model and returns the AI-generated response.
```
Example

```
!ai What is the meaning of life?
Response: "The meaning of life is subjective and depends on individual values and beliefs..."
```

# Contributing
Feel free to submit issues or pull requests if you want to contribute to the project.

# If this project is helpful, please give a star to this repository!

# License
This project is licensed under the MIT License.
