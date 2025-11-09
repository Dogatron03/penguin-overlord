# 🔑 How to Get a Discord Bot Token - Step-by-Step Guide

This guide will walk you through creating a Discord bot and getting your bot token.

## Step 1: Go to Discord Developer Portal

1. Open your web browser and go to: **https://discord.com/developers/applications**
2. Log in with your Discord account

## Step 2: Create a New Application

1. Click the **"New Application"** button (top right)
2. Give your application a name (e.g., "Penguin Overlord")
3. Read and accept the Developer Terms of Service
4. Click **"Create"**

## Step 3: Add a Bot to Your Application

1. In the left sidebar, click on **"Bot"**
2. Click the **"Add Bot"** button
3. Confirm by clicking **"Yes, do it!"**

🎉 Congratulations! Your bot is now created!

## Step 4: Get Your Bot Token

1. You should now see a "TOKEN" section
2. Click **"Reset Token"** (if this is your first time) or **"Copy"**
3. **⚠️ IMPORTANT:** Copy this token and save it securely!
   - This token is like a password - keep it secret!
   - You'll only see it once - if you lose it, you'll need to reset it
   - Never share it publicly or commit it to Git!

Your token will look something like this:
```
YOUR_BOT_TOKEN.HERE.EXAMPLE_TOKEN_DO_NOT_USE
```

## Step 5: Configure Bot Settings

While you're here, configure these important settings:

### Public Bot (Optional)
- Uncheck **"Public Bot"** if you only want to add it to your own servers
- Leave it checked if you want others to be able to invite your bot

### Privileged Gateway Intents (REQUIRED!)
Scroll down to **"Privileged Gateway Intents"** and enable:
- ✅ **MESSAGE CONTENT INTENT** - Required for the bot to read messages!
- ✅ **SERVER MEMBERS INTENT** (optional, for member-related features)
- ✅ **PRESENCE INTENT** (optional, for user status features)

**⚠️ Important:** The MESSAGE CONTENT INTENT is REQUIRED or the bot won't work!

## Step 6: Invite Your Bot to a Server

Now you need to invite your bot to a Discord server where you have admin permissions.

### Important Note About Private Bots

If you set your bot as **Private** (Public Bot unchecked in Step 5), you **cannot use the default authorization link** in the "Installation" tab. Instead, you **must use the OAuth2 URL Generator**.

### Generate Invite Link (Required for Private Bots)

1. In the left sidebar, go to **"OAuth2"** → **"URL Generator"**

2. Under **"SCOPES"**, check:
   - ✅ `bot`
   - ✅ `applications.commands` (for slash commands)

3. Under **"BOT PERMISSIONS"**, check these permissions:

   **Required for Penguin Overlord:**
   - ✅ **View Channels** (Read Messages/View Channels) - Bot needs to see channels
   - ✅ **Send Messages** - Post comics and responses
   - ✅ **Embed Links** - Display rich XKCD comic embeds
   - ✅ **Attach Files** - For future features (images, etc.)
   - ✅ **Use Slash Commands** (This is included in applications.commands scope)
   
   **Recommended (for scheduled posts & future features):**
   - ✅ **Read Message History** - For context in commands
   - ✅ **Add Reactions** - For interactive features
   - ✅ **Send Messages in Threads** - Post in thread discussions
   - ✅ **Manage Messages** - For future moderation features (optional)
   
   **Permissions Breakdown:**
   - **Text Permissions:** View Channels, Send Messages, Send Messages in Threads, Embed Links, Attach Files, Read Message History, Add Reactions
   - **Numeric Permission Value:** `414464724032` (if you need to set it manually)

4. Copy the generated URL at the bottom (it will look like):
   ```
   https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=414464724032&scope=bot%20applications.commands
   ```

5. Open the URL in your browser

6. Select the server you want to add the bot to

7. Click **"Authorize"**

8. Complete the CAPTCHA if prompted

🎉 Your bot is now in your server!

### Note: Why Private Bots Need OAuth2 URL Generator

- **Private bots** (Public Bot disabled) can only be invited by the bot owner
- The default authorization link in "Installation" only works for **public bots**
- You must manually generate an OAuth2 URL and use it yourself
- This gives you more control over where your bot is installed

## Step 7: Add Token to Penguin Overlord

Now add your token to the bot configuration:

### Option A: Using Doppler (Recommended)

1. Go to your Doppler dashboard
2. Select your project (e.g., "penguin-overlord")
3. Select your config (e.g., "prd")
4. Click **"Add Secret"**
5. Add:
   - **Name**: `DISCORD_BOT_TOKEN`
   - **Value**: (paste your token here)
6. Save

Then set your environment variables:
```bash
export DOPPLER_TOKEN=dp.st.your_doppler_token
export DOPPLER_PROJECT=penguin-overlord
export DOPPLER_CONFIG=prd
```

### Option B: Using .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file:
   ```bash
   nano .env
   # or
   vim .env
   ```

3. Replace `your_bot_token_here` with your actual token:
   ```
   DISCORD_BOT_TOKEN=your_bot_token_here
   ```

4. Save and close the file

**⚠️ Security Note:** Make sure `.env` is in your `.gitignore` file (it already is!)

## Step 8: Test Your Configuration

Run the test script to verify everything is set up:

```bash
python test_secrets.py
```

You should see:
```
✅ Successfully retrieved DISCORD_BOT_TOKEN!
   Token preview: MTIzNDU2Nzg5MDEyMzQ1...uvWx
   Token length: 72 characters
   Token format looks valid ✓
```

## Step 9: Start Your Bot!

```bash
./start.sh
```

Or manually:
```bash
cd penguin-overlord
python bot.py
```

You should see:
```
🐧 PenguinOverlord#1234 has connected to Discord!
Bot is in 1 guild(s)
```

## Step 10: Test the Bot in Discord

Go to your Discord server and try:
```
!xkcd
```

The bot should respond with the latest XKCD comic! 🎉

## Troubleshooting

### "Invalid Bot Token" Error
- Double-check you copied the entire token (no spaces or line breaks)
- Make sure you copied from the "TOKEN" section, not the Application ID
- Try resetting the token and getting a new one

### Bot Appears Offline
- Check that the token is correct
- Verify MESSAGE CONTENT INTENT is enabled
- Make sure your internet connection is working

### Bot Doesn't Respond to Commands
- Verify MESSAGE CONTENT INTENT is enabled (this is the most common issue!)
- Check the bot has permission to read and send messages in the channel
- Make sure you're using the correct prefix (`!`)

### "DISCORD_BOT_TOKEN not found" Error
- Verify your `.env` file exists and has the token
- If using Doppler, check `DOPPLER_TOKEN` is set: `echo $DOPPLER_TOKEN`
- Run `python test_secrets.py` to diagnose

## Security Best Practices

🔒 **DO:**
- Keep your token secret
- Use environment variables or secrets managers
- Rotate tokens periodically
- Use Doppler or similar for production

🚫 **DON'T:**
- Commit tokens to Git
- Share tokens in screenshots or logs
- Post tokens in Discord or forums
- Hardcode tokens in your source code

## Token Reset

If you accidentally exposed your token:

1. Go to Discord Developer Portal → Your App → Bot
2. Click **"Reset Token"**
3. Copy the new token
4. Update it in your configuration (Doppler or `.env`)
5. Restart your bot

## Additional Resources

- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Bot Best Practices](https://discord.com/developers/docs/topics/oauth2)
- [Message Content Intent Info](https://support-dev.discord.com/hc/en-us/articles/4404772028055)

## Quick Reference Card

| Step | Action | Result |
|------|--------|--------|
| 1 | Go to Discord Developer Portal | Access bot creation |
| 2 | Create New Application | Get application |
| 3 | Add Bot | Create bot user |
| 4 | Copy Token | Get bot token |
| 5 | Enable MESSAGE CONTENT INTENT | Bot can read messages |
| 6 | Generate OAuth2 URL | Get invite link |
| 7 | Add bot to server | Bot joins server |
| 8 | Add token to config | Bot can authenticate |
| 9 | Start bot | Bot comes online |
| 10 | Test with !xkcd | Bot responds! |

---

Need help? Run `python test_secrets.py` to diagnose configuration issues!

Made with 🐧 and ❤️
