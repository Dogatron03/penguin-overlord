# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Patch Gremlin Cog - Chaotic reminders about system updates.
"""

import logging
import random
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


# Chaotic update reminder messages
PATCH_GREMLINS = [
    {"msg": "🧌 PATCH GREMLIN SAYS: Your kernel is older than that milk in the back of your fridge.", "chaos": 3},
    {"msg": "🧌 PATCH GREMLIN SAYS: 247 updates available. But who's counting? (I am. I'm always counting.)", "chaos": 2},
    {"msg": "🧌 PATCH GREMLIN SAYS: That 'reboot required' flag has been there for 87 days. Live dangerously, I respect that.", "chaos": 3},
    {"msg": "🧌 PATCH GREMLIN SAYS: Your system has more unpatched CVEs than I have fingers. I have a LOT of fingers.", "chaos": 4},
    {"msg": "🧌 PATCH GREMLIN SAYS: Windows Update wants to restart. It's been patient. Very patient. TOO PATIENT.", "chaos": 2},
    {"msg": "🧌 PATCH GREMLIN SAYS: apt-get update && apt-get upgrade. You know you should. I know you won't.", "chaos": 2},
    {"msg": "🧌 PATCH GREMLIN SAYS: Your uptime is impressive. Your security posture is not.", "chaos": 3},
    {"msg": "🧌 PATCH GREMLIN SAYS: Docker images from 2019? That's not vintage, that's just neglect.", "chaos": 3},
    {"msg": "🧌 PATCH GREMLIN SAYS: The last patch Tuesday you participated in was... *checks notes* ...never.", "chaos": 3},
    {"msg": "🧌 PATCH GREMLIN SAYS: Your package manager is crying. Can you hear it? Listen closely...", "chaos": 4},
    {"msg": "🧌 PATCH GREMLIN SAYS: EOL software is like expired medicine. Sure, it might still work, but...", "chaos": 3},
    {"msg": "🧌 PATCH GREMLIN SAYS: Zero-day? More like zero-days-since-you-last-patched.", "chaos": 4},
    {"msg": "🧌 PATCH GREMLIN SAYS: I see you're running PHP 5.6. Bold strategy, Cotton.", "chaos": 5},
    {"msg": "🧌 PATCH GREMLIN SAYS: Your SSL certificate expires in 3 days. Sleep well!", "chaos": 5},
    {"msg": "🧌 PATCH GREMLIN SAYS: 'yum update' or 'dnf upgrade'? The real question is: will you run either?", "chaos": 2},
    {"msg": "🧌 PATCH GREMLIN SAYS: Automatic updates are disabled. Living on the edge, I see.", "chaos": 3},
    {"msg": "🧌 PATCH GREMLIN SAYS: That npm package hasn't been updated in 4 years. It's fine. Everything is fine.", "chaos": 3},
    {"msg": "🧌 PATCH GREMLIN SAYS: Your dependencies have dependencies that have vulnerabilities. It's turtles all the way down.", "chaos": 4},
    {"msg": "🧌 PATCH GREMLIN SAYS: Log4Shell called. It wants to know why you still haven't patched.", "chaos": 5},
    {"msg": "🧌 PATCH GREMLIN SAYS: Remember Heartbleed? Your OpenSSL version does.", "chaos": 4},
    
    # Less chaotic, more helpful
    {"msg": "🧌 Patch Gremlin reminder: Regular updates keep the security demons away!", "chaos": 1},
    {"msg": "🧌 Patch Gremlin reminder: Check for updates today. Your future self will thank you.", "chaos": 1},
    {"msg": "🧌 Patch Gremlin reminder: Windows Update Tuesday is a feature, not a bug.", "chaos": 1},
    {"msg": "🧌 Patch Gremlin reminder: sudo apt update && sudo apt upgrade - Make it a habit!", "chaos": 1},
    {"msg": "🧌 Patch Gremlin reminder: Patch management is like brushing your teeth. Do it regularly or things get ugly.", "chaos": 1},
    {"msg": "🧌 Patch Gremlin reminder: Your system is only as secure as your oldest unpatched package.", "chaos": 2},
    {"msg": "🧌 Patch Gremlin reminder: Reboot after kernel updates. Your uptime badge isn't worth a breach.", "chaos": 2},
    {"msg": "🧌 Patch Gremlin reminder: Check CVE databases for your running software. Knowledge is power!", "chaos": 1},
    {"msg": "🧌 Patch Gremlin reminder: Enable automatic security updates. Sleep better at night.", "chaos": 1},
    {"msg": "🧌 Patch Gremlin reminder: Test patches in dev before production. But DO patch production.", "chaos": 1},
]


class PatchGremlin(commands.Cog):
    """Patch Gremlin - Chaotic update reminders."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='patchgremlin', description='Get a chaotic reminder about updates')
    async def patchgremlin(self, ctx: commands.Context):
        """
        The Patch Gremlin reminds you about system updates in a chaotic way.
        Sometimes helpful, sometimes sarcastic, always memorable.
        
        Usage:
            !patchgremlin
            /patchgremlin
        """
        gremlin_data = random.choice(PATCH_GREMLINS)
        
        # Color based on chaos level
        if gremlin_data['chaos'] >= 4:
            color = 0xFF1744  # Bright red for high chaos
        elif gremlin_data['chaos'] >= 3:
            color = 0xFF6F00  # Orange for medium chaos
        elif gremlin_data['chaos'] >= 2:
            color = 0xFFD600  # Yellow for mild chaos
        else:
            color = 0x00E676  # Green for helpful
        
        embed = discord.Embed(
            title="🧌 Patch Gremlin Alert",
            description=gremlin_data['msg'],
            color=color
        )
        
        # Add footer with chaos level
        chaos_meter = "🔥" * gremlin_data['chaos']
        embed.set_footer(text=f"Chaos Level: {chaos_meter} • Use !patchgremlin for more reminders")
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Load the PatchGremlin cog."""
    await bot.add_cog(PatchGremlin(bot))
    logger.info("PatchGremlin cog loaded")
