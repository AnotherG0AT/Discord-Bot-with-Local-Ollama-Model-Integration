# Tutorial: Building a Discord Bot with Local Ollama Model Integration
A guide and template for building a Discord bot that connects to locally installed AI models from Ollama using a local API. This project is perfect for developers looking to integrate AI features into their bots with local model inference.

# Requirements

Python 3.8+
Ollama (with models installed)
Git
Discord Developer Token
discord.py library
python-dotenv for environment variable management
requests library to handle API calls


Clone the repository:

```
git clone https://github.com/your-username/discord-bot-ollama-model-integration.git
cd discord-bot-ollama-model-integration
```

Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```
Set up the environment variables:

Create a .env file in the root directory of the project.
Add your Discord bot token and the Ollama API URL:

```
DISCORD_TOKEN=your-discord-bot-token
OLLAMA_API_URL=http://localhost:11434
```

Running the Bot

Start the Ollama API: Ensure your local Ollama API is running on http://localhost:11434.

Run the bot:
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

Contributing
Feel free to submit issues or pull requests if you want to contribute to the project.

License
This project is licensed under the MIT License.
