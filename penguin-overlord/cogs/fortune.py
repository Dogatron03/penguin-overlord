# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Fortune Cog - Cyber Fortune Cookie with infosec wisdom (sarcastic and real).
"""

import logging
import random
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


# Cyber Fortune Cookie quotes - mix of sarcastic and real infosec wisdom
CYBER_FORTUNES = [
    # Sarcastic wisdom
    {"quote": "Your password is strong. So strong that even you can't remember it.", "sarcastic": True},
    {"quote": "A SQL injection walks into a bar. The bartender says, 'We don't serve your kind here.' The injection replies, 'That's OK, I brought my own table.'", "sarcastic": True},
    {"quote": "Remember: The 'S' in IoT stands for Security.", "sarcastic": True},
    {"quote": "Your two-factor authentication is working perfectly. Both factors are equally vulnerable.", "sarcastic": True},
    {"quote": "Congratulations! You've been using the same password since 2008. Consistency is key.", "sarcastic": True},
    {"quote": "The cloud is just someone else's computer. And they're probably as bad at security as you are.", "sarcastic": True},
    {"quote": "Your API keys are safe in that public GitHub repo. Nobody reads documentation anyway.", "sarcastic": True},
    {"quote": "Don't worry about that certificate error. What's the worst that could happen?", "sarcastic": True},
    {"quote": "Your firewall is working great. It's blocking everything except the hackers.", "sarcastic": True},
    {"quote": "Yes, admin/admin is a perfectly reasonable default credential. It's easy to remember!", "sarcastic": True},
    {"quote": "That suspicious email from 'IT Department' asking for your password? Totally legit.", "sarcastic": True},
    {"quote": "Your company's security is like a screen door on a submarine. But at least you have one!", "sarcastic": True},
    {"quote": "Penetration testing is just hacking with permission and a invoice.", "sarcastic": True},
    {"quote": "Your database backup strategy: Hope nothing bad happens.", "sarcastic": True},
    {"quote": "Security through obscurity works great. Until someone Googles it.", "sarcastic": True},
    
    # Real infosec wisdom
    {"quote": "The only truly secure system is one that is powered off, cast in a block of concrete and sealed in a lead-lined room with armed guards. - Gene Spafford", "sarcastic": False},
    {"quote": "In security, the key is not to have all the answers but to ask the right questions. - Marcus Ranum", "sarcastic": False},
    {"quote": "Passwords are like underwear: you don't let people see it, you should change it regularly, and you shouldn't share it with strangers. - Chris Pirillo", "sarcastic": False},
    {"quote": "If you spend more on coffee than on IT security, you will be hacked. What's more, you deserve to be hacked. - Richard Clarke", "sarcastic": False},
    {"quote": "There are two types of companies: those that have been hacked, and those that don't know they've been hacked.", "sarcastic": False},
    {"quote": "Security is always excessive until it's not enough. - Robbie Sinclair", "sarcastic": False},
    {"quote": "The weakest link in any security chain is the human element.", "sarcastic": False},
    {"quote": "Defense in depth: Because one layer of security is just a speed bump for attackers.", "sarcastic": False},
    {"quote": "Assume breach. It's not paranoia if they're really out to get you.", "sarcastic": False},
    {"quote": "You can't protect what you don't know you have. Asset inventory is security 101.", "sarcastic": False},
    {"quote": "Encryption is the mathematical guarantee of security. Implementation is the engineering guarantee of failure.", "sarcastic": False},
    {"quote": "Zero trust: Verify everything, trust nothing.", "sarcastic": False},
    {"quote": "A backup is only as good as its last successful restore.", "sarcastic": False},
    {"quote": "Incident response: Because 'when' is more realistic than 'if'.", "sarcastic": False},
    {"quote": "Patch management: The only thing worse than applying patches is not applying patches.", "sarcastic": False},
    {"quote": "Your security posture should be good enough to make attackers choose easier targets.", "sarcastic": False},
    {"quote": "Security awareness training: Because humans are both your greatest strength and your biggest vulnerability.", "sarcastic": False},
    {"quote": "Defense requires vigilance. Offense just needs one mistake.", "sarcastic": False},
    {"quote": "Logging: The difference between knowing you were hacked and proving you were hacked.", "sarcastic": False},
    {"quote": "Multi-factor authentication: Because one factor is no longer enough.", "sarcastic": False},
]


class Fortune(commands.Cog):
    """Cyber Fortune Cookie - Infosec wisdom with a twist."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='fortune', description='Get a cyber fortune cookie')
    async def fortune(self, ctx: commands.Context):
        """
        Get a random cyber fortune cookie with infosec wisdom.
        Can be sarcastic or genuinely helpful!
        
        Usage:
            !fortune
            /fortune
        """
        fortune_data = random.choice(CYBER_FORTUNES)
        
        # Create embed with different colors for sarcastic vs real wisdom
        color = 0xFF6B6B if fortune_data['sarcastic'] else 0x4ECDC4
        wisdom_type = "🍪 Sarcastic Wisdom" if fortune_data['sarcastic'] else "🔐 Real Wisdom"
        
        embed = discord.Embed(
            title=wisdom_type,
            description=fortune_data['quote'],
            color=color
        )
        
        embed.set_footer(text="Cyber Fortune Cookie • Use !fortune for more wisdom")
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Load the Fortune cog."""
    await bot.add_cog(Fortune(bot))
    logger.info("Fortune cog loaded")
