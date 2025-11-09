# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Manpage Cog - Random Linux command snippets from man pages.
"""

import logging
import random
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


# Random useful Linux commands with descriptions
LINUX_COMMANDS = [
    {"cmd": "dd if=/dev/zero of=/dev/null", "desc": "The world's most efficient space heater. Does absolutely nothing but looks impressive.", "danger": 1},
    {"cmd": ":(){ :|:& };:", "desc": "Fork bomb. Also known as 'the rabbit function'. DO NOT RUN THIS. It will crash your system.", "danger": 5},
    {"cmd": "sudo rm -rf /", "desc": "The nuclear option. Deletes everything. Please don't actually run this.", "danger": 5},
    {"cmd": "cat /dev/urandom | hexdump | grep 'ca fe'", "desc": "Looking for coffee in random data. You'll find it eventually... probably.", "danger": 1},
    {"cmd": "alias please='sudo'", "desc": "Politeness matters, even with your terminal.", "danger": 1},
    {"cmd": "sl", "desc": "Like 'ls', but with more trains. Install with apt-get install sl", "danger": 1},
    {"cmd": "telnet towel.blinkenlights.nl", "desc": "Watch Star Wars in ASCII art. Yes, really.", "danger": 1},
    {"cmd": "nc -l 1337", "desc": "Listen on port 1337 like a true 1337 h4x0r.", "danger": 1},
    {"cmd": "curl parrot.live", "desc": "Watch a dancing parrot in your terminal. Essential system administration.", "danger": 1},
    {"cmd": "sudo !!", "desc": "Forgot sudo? This runs your last command with sudo. Time saver!", "danger": 2},
    
    # Actually useful commands
    {"cmd": "grep -r 'pattern' /path", "desc": "Search for text recursively. Your best friend for finding that one config line.", "danger": 1},
    {"cmd": "find . -name '*.log' -mtime +30 -delete", "desc": "Delete log files older than 30 days. Spring cleaning for your disk.", "danger": 3},
    {"cmd": "rsync -avz source/ dest/", "desc": "Copy files with progress, resume support, and style. Better than cp.", "danger": 1},
    {"cmd": "tar -xzf archive.tar.gz", "desc": "Extract a gzipped tarball. Memorize this, you'll use it forever.", "danger": 1},
    {"cmd": "netstat -tulpn", "desc": "See what's listening on your ports. Great for finding rogue services.", "danger": 1},
    {"cmd": "ps aux | grep process", "desc": "Find a running process. The aux flags are muscle memory for sysadmins.", "danger": 1},
    {"cmd": "du -sh *", "desc": "See which directories are eating your disk space. Prepare to be surprised.", "danger": 1},
    {"cmd": "htop", "desc": "Like top, but prettier. Install it. Love it. Never go back.", "danger": 1},
    {"cmd": "tail -f /var/log/syslog", "desc": "Watch logs in real-time. Perfect for debugging or pretending to work.", "danger": 1},
    {"cmd": "chmod +x script.sh", "desc": "Make a script executable. One of the first things you Google as a Linux newbie.", "danger": 1},
    {"cmd": "ssh -L 8080:localhost:80 user@host", "desc": "SSH tunnel magic. Access remote services like they're local.", "danger": 1},
    {"cmd": "screen", "desc": "Detachable terminal sessions. Your work survives even if SSH doesn't.", "danger": 1},
    {"cmd": "tmux", "desc": "Like screen, but newer and with more features. Start the holy war in the comments.", "danger": 1},
    {"cmd": "awk '{print $1}' file.txt", "desc": "Extract the first column. AWK is a Swiss Army chainsaw.", "danger": 1},
    {"cmd": "sed 's/old/new/g' file.txt", "desc": "Find and replace text. sed is the editor you never knew you needed.", "danger": 1},
    {"cmd": "journalctl -xe", "desc": "Read systemd logs. Because systemd owns your boot process now.", "danger": 1},
    {"cmd": "df -h", "desc": "Check disk space in human-readable format. Always run this before 'disk full' errors.", "danger": 1},
    {"cmd": "free -h", "desc": "Check memory usage. Yes, Linux is using all your RAM as cache. It's fine.", "danger": 1},
    {"cmd": "lsof -i :80", "desc": "See what's using port 80. Process detective work.", "danger": 1},
    {"cmd": "strace -p PID", "desc": "See what a process is doing at the syscall level. For when debugging gets serious.", "danger": 1},
]


class Manpage(commands.Cog):
    """Random Linux Command Bot - Man page snippets."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='manpage', description='Get a random Linux command')
    async def manpage(self, ctx: commands.Context):
        """
        Get a random Linux command with description.
        May include both useful and dangerous commands - use with caution!
        
        Usage:
            !manpage
            /manpage
        """
        cmd_data = random.choice(LINUX_COMMANDS)
        
        # Color based on danger level
        if cmd_data['danger'] >= 4:
            color = 0xFF0000  # Red for dangerous
            danger_emoji = "☠️"
        elif cmd_data['danger'] >= 3:
            color = 0xFF6B00  # Orange for caution
            danger_emoji = "⚠️"
        else:
            color = 0x00D166  # Green for safe
            danger_emoji = "✅"
        
        embed = discord.Embed(
            title=f"{danger_emoji} Random Linux Command",
            color=color
        )
        
        embed.add_field(name="Command", value=f"`{cmd_data['cmd']}`", inline=False)
        embed.add_field(name="Description", value=cmd_data['desc'], inline=False)
        
        if cmd_data['danger'] >= 4:
            embed.add_field(
                name="⚠️ WARNING ⚠️", 
                value="This command is dangerous! Do NOT run it unless you know exactly what you're doing!", 
                inline=False
            )
        
        embed.set_footer(text="man page • Use !manpage for more commands")
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Load the Manpage cog."""
    await bot.add_cog(Manpage(bot))
    logger.info("Manpage cog loaded")
