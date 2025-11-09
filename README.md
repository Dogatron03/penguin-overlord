# 🐧 Penguin Overlord

A fun Discord bot with XKCD comics and Tech Quotes from legends in computer science, open source, and technology!

## Features

### 💬 Tech Quote of the Day
Get inspirational, humorous, and insightful quotes from tech legends!

**Commands:**
- `!techquote` or `/techquote` - Get a random quote from any tech legend
- `!quote_linus` or `/quote_linus` - Get a quote from Linus Torvalds
- `!quote_stallman` or `/quote_stallman` - Get a quote from Richard Stallman
- `!quote_hopper` or `/quote_hopper` - Get a quote from Grace Hopper
- `!quote_shevinsky` or `/quote_shevinsky` - Get a quote from Elissa Shevinsky
- `!quote_may` or `/quote_may` - Get a quote from Timothy C. May
- `!quote_list` or `/quote_list` - Browse all available quote authors (interactive paginator!)

**Featured Quote Authors (610+ quotes from 70+ legends):**
- Linux/Unix Pioneers: Linus Torvalds, Dennis Ritchie, Ken Thompson, Rob Pike
- Open Source Champions: Richard Stallman, Eric S. Raymond, Larry Wall
- Language Creators: Guido van Rossum (Python), Yukihiro Matsumoto (Ruby), Bjarne Stroustrup (C++)
- Computer Science Legends: Alan Turing, Ada Lovelace, Grace Hopper, Donald Knuth, Edsger Dijkstra
- Industry Icons: Steve Jobs, Bill Gates, Mark Zuckerberg
- Privacy & Security: Elissa Shevinsky, Timothy C. May, Gene Spafford
- Software Engineering: Fred Brooks, Robert C. Martin, Martin Fowler, Kent Beck
- And many more!

### 🎨 XKCD Commands
- `!xkcd` or `!xkcd [number]` - Get the latest XKCD comic or a specific one by number
- `!xkcd_latest` - Get the latest XKCD comic
- `!xkcd_random` - Get a random XKCD comic
- `!xkcd_search [keyword]` - Search for XKCD comics by keyword in titles (searches last 100 comics)

All commands support both prefix (`!command`) and slash commands (`/command`)!

## Setup

### Prerequisites
- Python 3.8 or higher
- A Discord account
- A Discord bot token

### Getting a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "Penguin Overlord")
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under the "Token" section, click "Copy" to copy your bot token
6. **Important**: Enable "Message Content Intent" under Privileged Gateway Intents

### Inviting the Bot to Your Server

1. In the Discord Developer Portal, go to the "OAuth2" > "URL Generator" section
2. Select the following scopes:
   - `bot`
   - `applications.commands`
3. Select the following bot permissions:
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
   - Attach Files
   - Use Slash Commands
4. Copy the generated URL and open it in your browser
5. Select the server you want to add the bot to and authorize it

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd penguin-overlord
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Choose your configuration method:**

   **Option A: Using Doppler (Recommended for Production)**
   
   The bot integrates with Doppler secrets manager. If you have a `DOPPLER_TOKEN` set, it will automatically fetch secrets from Doppler.
   
   ```bash
   # Set Doppler token
   export DOPPLER_TOKEN=your_doppler_token
   export DOPPLER_PROJECT=penguin-overlord
   export DOPPLER_CONFIG=prd
   ```
   
   In your Doppler project, add the secret:
   - `DISCORD_BOT_TOKEN` - Your Discord bot token
   
   **Option B: Using .env file (Simple Setup)**
   
   ```bash
   cp .env.example .env
   # Edit .env and add your Discord bot token
   ```
   
   **Option C: AWS Secrets Manager**
   
   Set `SECRETS_MANAGER=aws` and configure AWS credentials
   
   **Option D: HashiCorp Vault**
   
   Set `SECRETS_MANAGER=vault` and configure Vault credentials

### Quick Start (Automated)

The easiest way to get started:

```bash
./start.sh
```

This script will:
1. Create a virtual environment (if needed)
2. Install all dependencies
3. Test your configuration
4. Start the bot

### Testing Your Configuration

Before running the bot manually, test that your secrets are configured correctly:

```bash
python test_secrets.py
```

This will verify:
- ✅ Doppler connection (if using Doppler)
- ✅ Discord bot token retrieval
- ✅ Token format validation
- ✅ Configuration sources

### Running the Bot (Manual)

From the `penguin-overlord` directory:

```bash
python -m penguin-overlord.bot
```

Or from the main project directory:

```bash
cd penguin-overlord
python bot.py
```

**With Doppler CLI:**

```bash
doppler run -- python bot.py
```

You should see:
```
🐧 [YourBot#1234] has connected to Discord!
```

## Development

### Project Structure

```
penguin-overlord/
├── penguin-overlord/
│   ├── bot.py           # Main bot entry point
│   ├── cogs/            # Bot extensions/features
│   │   ├── xkcd.py      # XKCD commands
│   │   ├── techquote.py # Tech Quote commands (610+ quotes!)
│   │   └── admin.py     # Admin commands
│   ├── social/          # Social platform integrations
│   │   ├── discord.py   # Discord webhook platform
│   │   └── matrix.py    # Matrix platform (future)
│   └── utils/           # Utility modules
│       ├── config.py    # Configuration management
│       └── secrets.py   # Secrets management
├── requirements.txt     # Python dependencies
├── .env.example        # Example environment variables
└── README.md           # This file
```

### Adding New Features

To add a new feature/command set:

1. Create a new cog file in `penguin-overlord/cogs/`
2. Follow the pattern in `xkcd.py`
3. The bot will automatically load it on startup!

Example cog structure:
```python
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command()
    async def mycommand(self, ctx):
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

### Current Features
- ✅ XKCD comic integration with search
- ✅ Tech Quote of the Day (610+ quotes from 70+ tech legends)
- ✅ Interactive paginator for browsing quotes
- ✅ Hybrid commands (both prefix and slash commands)
- ✅ Doppler secrets management integration

### Future Features
- 🔲 Matrix bot integration
- 🔲 Scheduled daily tech quotes
- 🔲 More fun commands
- 🔲 Games and interactive features
- 🔲 Moderation tools
- 🔲 Custom per-server configurations

## License

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Support

If you encounter any issues or have questions:
1. Check that your bot token is correct
2. Make sure the bot has the necessary permissions in your Discord server
3. Check the console logs for error messages
4. Ensure you've enabled "Message Content Intent" in the Discord Developer Portal

---

Made with 🐧 and ❤️
