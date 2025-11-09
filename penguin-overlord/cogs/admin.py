# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Admin Cog - Administrative commands for bot management.
"""

import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class Admin(commands.Cog):
    """Administrative commands - owner only."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='sync', hidden=True)
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        """
        Manually sync slash commands with Discord (owner only).
        
        Usage:
            !sync - Sync commands globally
        """
        await ctx.send("🔄 Syncing slash commands...")
        
        try:
            synced = await self.bot.tree.sync()
            await ctx.send(f"✅ Successfully synced {len(synced)} slash command(s)!")
            logger.info(f"Manual sync: {len(synced)} commands synced by {ctx.author}")
        except Exception as e:
            await ctx.send(f"❌ Failed to sync commands: {e}")
            logger.error(f"Manual sync failed: {e}")


async def setup(bot):
    """Load the Admin cog."""
    await bot.add_cog(Admin(bot))
    logger.info("Admin cog loaded")
