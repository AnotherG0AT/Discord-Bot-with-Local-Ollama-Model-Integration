import discord
from discord.ext import commands
import youtube_dl
import requests
import json
import random

# Your bot token
DISCORD_TOKEN = 'your discord bot token'

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store user balances for the economy system
user_balances = {}

# Dictionary to store command descriptions
command_descriptions = {
    '!ask [question]': 'Send a question or prompt to the AI model and get a response.',
    '!ai [question]': 'Alias for !ask.',
    '!dwiscord [question]': 'Alias for !ask.',
    '?ai [question]': 'Alias for !ask.',
    '!roll': 'Roll a random number between 1 and 100.',
    '!flip': 'Flip a virtual coin (Heads or Tails).',
    '!joke': 'Tell a random joke.',
    '!meme': 'Share a random meme image.',
    '!8ball [question]': 'Get a magic 8-ball style response to a question.',
    '!hug': 'Send a virtual hug to the user.',
    '!slap': 'Send a virtual slap to the user.',
    '!ttt [position]': 'Play a move in Tic-Tac-Toe (position from 1 to 9).',
    '!rps [choice]': 'Play Rock-Paper-Scissors (choice: rock, paper, or scissors).',
    '!balance': 'Check your coin balance.',
    '!earn': 'Earn a random amount of coins.',
    '!spend [amount]': 'Spend a specified amount of coins.',
    '!status [status]': 'Change the bot’s status.',
    '!weather [city]': 'Get the current weather for a specified city.',
    '!join': 'Make the bot join the voice channel you’re in.',
    '!play [url]': 'Play audio from a YouTube URL in the voice channel.',
    '!ban [member] [reason]': 'Ban a member from the server.',
    '!unban [member]': 'Unban a member from the server.',
    '!commands': 'List all available commands and their descriptions.'
}

# Function to get response from the Ollama model
def get_ollama_response(prompt, model="your model id here"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt
    }
    
    full_response = ""
    try:
        with requests.post(url, json=data, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    full_response += json_response.get('response', '')
                    if json_response.get('done', False):
                        break
    except requests.RequestException as e:
        return f"Error communicating with Ollama: {str(e)}"
    
    return full_response.strip()

# Welcome message on bot startup
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = discord.utils.get(client.get_all_channels(), name='general')
    if channel:
        await channel.send("Hello, I am alive!")

# Respond to messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Economy system: Initial balance
    user_id = message.author.id
    if user_id not in user_balances:
        user_balances[user_id] = 100  # Initial balance
    
    # Frog infection message
    if "frog" in message.content.lower():
        infection_message = (
            "Welcome to the new epidemic. If you fail to participate, you will bring shame onto Discord and all frog kind. "
            "You have been infected. Now change your status to 'DM me the word frog for a surprise.' "
            "The infection shall spread silently. The only rule is to not spoil the game for others by telling people what saying frog does. "
            "You have to keep the status forever."
        )
        await message.channel.send(infection_message)
        return

    # General AI response
    if message.content.startswith(('!ask', '!ai', 'dwiscord', '?ai')):
        query = message.content.split(' ', 1)[1].strip() if ' ' in message.content else ""
        if query:
            try:
                ai_response = get_ollama_response(query)
                # Split long responses into multiple messages if needed
                while ai_response:
                    await message.channel.send(ai_response[:2000])
                    ai_response = ai_response[2000:]
            except Exception as e:
                await message.channel.send(f"An error occurred: {str(e)}")
        else:
            await message.channel.send("Please ask a question after the command.")
        return
    
    # Fun commands
    if message.content.lower().startswith('!roll'):
        roll_result = random.randint(1, 100)
        await message.channel.send(f'🎲 You rolled a {roll_result}!')
    
    if message.content.lower().startswith('!flip'):
        flip_result = random.choice(['Heads', 'Tails'])
        await message.channel.send(f'🪙 You flipped {flip_result}!')

    if message.content.lower().startswith('!joke'):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call fake spaghetti? An impasta!"
        ]
        await message.channel.send(random.choice(jokes))
    
    if message.content.lower().startswith('!meme'):
        memes = [
            "https://i.imgur.com/w3duR07.png",
            "https://i.imgur.com/jIM7MPR.png",
            "https://i.imgur.com/2YlpeK6.png"
        ]
        await message.channel.send(random.choice(memes))

    if message.content.lower().startswith('!8ball'):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes – definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        await message.channel.send(f"🎱 {random.choice(responses)}")

    if message.content.lower().startswith('!hug'):
        await message.channel.send(f'{message.author.mention} hugs you!')

    if message.content.lower().startswith('!slap'):
        await message.channel.send(f'{message.author.mention} slaps you!')

    if message.content.lower().startswith('!ttt'):
        pos = int(message.content.split(' ')[1]) - 1  # Get the position from the command
        if move('X', pos):
            if check_win('X'):
                await message.channel.send("X wins!\n" + print_board())
                tictactoe_board[:] = [' ' for _ in range(9)]
            else:
                await message.channel.send(print_board())
        else:
            await message.channel.send("Invalid move.")
    
    if message.content.lower().startswith('!rps'):
        user_choice = message.content.split(' ')[1].lower()
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(choices)

        if user_choice == bot_choice:
            result = "It's a tie!"
        elif (user_choice == 'rock' and bot_choice == 'scissors') or \
             (user_choice == 'scissors' and bot_choice == 'paper') or \
             (user_choice == 'paper' and bot_choice == 'rock'):
            result = f'You win! Bot chose {bot_choice}.'
        else:
            result = f'You lose! Bot chose {bot_choice}.'

        await message.channel.send(result)
    
    if message.content.lower().startswith('!balance'):
        await message.channel.send(f"{message.author.mention}, you have {user_balances[user_id]} coins.")
    
    if message.content.lower().startswith('!earn'):
        coins = random.randint(10, 50)
        user_balances[user_id] += coins
        await message.channel.send(f"{message.author.mention} earned {coins} coins!")

    if message.content.lower().startswith('!spend'):
        coins = int(message.content.split(' ')[1])
        if user_balances[user_id] >= coins:
            user_balances[user_id] -= coins
            await message.channel.send(f"{message.author.mention} spent {coins} coins!")
        else:
            await message.channel.send(f"{message.author.mention}, you don't have enough coins!")
    
    if message.content.lower().startswith('!status'):
        new_status = message.content.split(' ', 1)[1]
        await client.change_presence(activity=discord.Game(new_status))
        await message.channel.send(f'Status changed to: {new_status}')
    
    if message.content.lower().startswith('!weather'):
        city = message.content.split(' ', 1)[1]
        api_key = 'YOUR_WEATHER_API_KEY'
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url).json()
        
        if response.get('cod') != 200:
            await message.channel.send(f"City {city} not found.")
        else:
            temp = response['main']['temp'] - 273.15  # Kelvin to Celsius
            await message.channel.send(f'Temperature in {city}: {temp:.2f}°C')

    # Handle !commands
    if message.content.lower().startswith('!commands'):
        command_list = '\n'.join([f'{cmd}: {desc}' for cmd, desc in command_descriptions.items()])
        await message.channel.send(f"**Available Commands:**\n{command_list}")

@client.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You're not connected to a voice channel.")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command()
async def play(ctx, url):
    server = ctx.message.guild
    voice_channel = server.voice_client

    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['url']
    voice_channel.play(discord.FFmpegPCMAudio(URL))

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

def move(player, position):
    if tictactoe_board[position] == ' ':
        tictactoe_board[position] = player
        return True
    return False

def check_win(player):
    win_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    return any(all(tictactoe_board[i] == player for i in combo) for combo in win_positions)

def print_board():
    board_visual = f"""
     {tictactoe_board[0]} | {tictactoe_board[1]} | {tictactoe_board[2]}
    -----------
     {tictactoe_board[3]} | {tictactoe_board[4]} | {tictactoe_board[5]}
    -----------
     {tictactoe_board[6]} | {tictactoe_board[7]} | {tictactoe_board[8]}
    """
    return board_visual

# Initialize the Tic Tac Toe board
tictactoe_board = [' ' for _ in range(9)]

# Run the bot
client.run(DISCORD_TOKEN)
