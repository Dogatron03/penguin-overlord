# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Cybersecurity News Cog - Aggregates cybersecurity and threat intelligence news.
"""

import logging
import discord
from discord.ext import commands, tasks
from discord import app_commands
import aiohttp
import re
import json
import os
from datetime import datetime
from html import unescape

logger = logging.getLogger(__name__)


NEWS_SOURCES = {
    '404media': {
        'name': '404 Media',
        'url': 'https://404media.co/rss/',
        'color': 0xFF6B35,
        'icon': '📰'
    },
    'arstechnica_sec': {
        'name': 'Ars Technica Security',
        'url': 'https://feeds.arstechnica.com/arstechnica/security',
        'color': 0xFF4F00,
        'icon': '🔬'
    },
    'thehackernews': {
        'name': 'The Hacker News',
        'url': 'https://thehackernews.com/feeds/posts/default',
        'color': 0xD9231F,
        'icon': '🔒'
    },
    'welivesecurity': {
        'name': 'WeLiveSecurity (ESET)',
        'url': 'https://www.welivesecurity.com/feed/',
        'color': 0x00A3E0,
        'icon': '🛡️'
    },
    'darkreading': {
        'name': 'Dark Reading',
        'url': 'https://www.darkreading.com/rss.xml',
        'color': 0x1A1A1A,
        'icon': '🌑'
    },
    'bleepingcomputer': {
        'name': 'BleepingComputer',
        'url': 'https://www.bleepingcomputer.com/feed/',
        'color': 0x0066CC,
        'icon': '💻'
    },
    'malwarebytes': {
        'name': 'Malwarebytes Labs',
        'url': 'https://blog.malwarebytes.com/feed/',
        'color': 0xFF6A13,
        'icon': '🦠'
    },
    'wired_security': {
        'name': 'Wired Security',
        'url': 'https://www.wired.com/category/security/feed',
        'color': 0x000000,
        'icon': '📡'
    },
    'eff': {
        'name': 'EFF Deeplinks',
        'url': 'https://www.eff.org/rss/updates.xml',
        'color': 0xC8102E,
        'icon': '🗽'
    },
    'schneier': {
        'name': 'Schneier on Security',
        'url': 'https://www.schneier.com/feed/atom/',
        'color': 0x8B4513,
        'icon': '📚'
    },
    'cyberscoop': {
        'name': 'CyberScoop',
        'url': 'https://www.cyberscoop.com/feed/',
        'color': 0x1E3A8A,
        'icon': '🏛️'
    },
    'securityweek': {
        'name': 'SecurityWeek',
        'url': 'https://feeds.feedburner.com/securityweek',
        'color': 0x2E5C8A,
        'icon': '📊'
    },
    'databreaches': {
        'name': 'DataBreaches.net',
        'url': 'https://www.databreaches.net/feed/',
        'color': 0xE74C3C,
        'icon': '💥'
    },
    'aws_security': {
        'name': 'AWS Security Blog',
        'url': 'https://aws.amazon.com/blogs/security/feed/',
        'color': 0xFF9900,
        'icon': '☁️'
    },
    'crowdstrike': {
        'name': 'CrowdStrike',
        'url': 'https://www.crowdstrike.com/blog/feed/',
        'color': 0xE01F3D,
        'icon': '🦅'
    },
    'tenable': {
        'name': 'Tenable',
        'url': 'https://www.tenable.com/blog/rss',
        'color': 0x00B2A9,
        'icon': '🔬'
    },
    'zscaler': {
        'name': 'Zscaler Research',
        'url': 'https://www.zscaler.com/blogs/feed',
        'color': 0x0066CC,
        'icon': '🌐'
    },
    'privacyintl': {
        'name': 'Privacy International',
        'url': 'https://privacyinternational.org/rss.xml',
        'color': 0x9B59B6,
        'icon': '🕵️‍♀️'
    }
}


class CybersecurityNews(commands.Cog):
    """Cybersecurity news aggregator and poster."""
    
    NEWS_SOURCES = NEWS_SOURCES
    
    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self.state_file = 'data/cybersecurity_news_state.json'
        self.state = self._load_state()
        self.news_auto_poster.start()
    
    def cog_unload(self):
        self.news_auto_poster.cancel()
        if self.session:
            self.bot.loop.create_task(self.session.close())
    
    async def cog_load(self):
        self.session = aiohttp.ClientSession()
    
    def _load_state(self) -> dict:
        """Load state from file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load cybersecurity news state: {e}")
        
        return {
            'last_posted': {},
            'last_check': None
        }
    
    def _save_state(self):
        """Save state to file."""
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save cybersecurity news state: {e}")
    
    async def _fetch_rss_feed(self, source_key: str) -> tuple[str, str, str]:
        """Fetch latest article from an RSS feed."""
        source = NEWS_SOURCES.get(source_key)
        if not source:
            return None, None, None
        
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(source['url'], timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    logger.warning(f"Failed to fetch {source['name']}: HTTP {response.status}")
                    return None, None, None
                
                content = await response.text()
                
                # Parse RSS/Atom feed
                item_pattern = r'<item>(.*?)</item>' if '<item>' in content else r'<entry>(.*?)</entry>'
                items = re.findall(item_pattern, content, re.DOTALL)
                
                if not items:
                    return None, None, None
                
                item = items[0]
                
                # Extract title
                title_match = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item, re.DOTALL)
                title = unescape(title_match.group(1).strip()) if title_match else "No title"
                
                # Extract link
                link_match = re.search(r'<link(?:\s+[^>]*)?>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>', item, re.DOTALL)
                if not link_match:
                    link_match = re.search(r'<link\s+href="([^"]+)"', item)
                link = link_match.group(1).strip() if link_match else source['url']
                
                # Extract description
                desc_match = re.search(r'<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>', item, re.DOTALL)
                if not desc_match:
                    desc_match = re.search(r'<summary>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</summary>', item, re.DOTALL)
                
                description = ""
                if desc_match:
                    desc = desc_match.group(1).strip()
                    desc = re.sub(r'<[^>]+>', '', desc)
                    desc = unescape(desc)
                    description = desc[:300] + "..." if len(desc) > 300 else desc
                
                return title, link, description
        
        except Exception as e:
            logger.error(f"Error fetching {source['name']}: {e}")
            return None, None, None
    
    @tasks.loop(hours=4)
    async def news_auto_poster(self):
        """Automatically post cybersecurity news."""
        try:
            manager = self.bot.get_cog('NewsManager')
            if not manager:
                return
            
            config = manager.get_category_config('cybersecurity')
            
            if not config.get('enabled'):
                return
            
            channel_id = config.get('channel_id')
            if not channel_id:
                return
            
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return
            
            # Update interval dynamically
            interval = config.get('interval_hours', 4)
            if interval != self.news_auto_poster.hours:
                self.news_auto_poster.change_interval(hours=interval)
            
            # Post from each enabled source
            for source_key in NEWS_SOURCES.keys():
                if not manager.is_source_enabled('cybersecurity', source_key):
                    continue
                
                title, link, description = await self._fetch_rss_feed(source_key)
                
                if not title or not link:
                    continue
                
                # Check if already posted
                if self.state['last_posted'].get(source_key) == link:
                    continue
                
                source = NEWS_SOURCES[source_key]
                
                embed = discord.Embed(
                    title=f"{source['icon']} {title}",
                    url=link,
                    description=description,
                    color=source['color'],
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text=f"Source: {source['name']}")
                
                try:
                    await channel.send(embed=embed)
                    self.state['last_posted'][source_key] = link
                    self._save_state()
                except Exception as e:
                    logger.error(f"Failed to post from {source['name']}: {e}")
        
        except Exception as e:
            logger.error(f"Error in cybersecurity news auto-poster: {e}")
    
    @news_auto_poster.before_loop
    async def before_news_auto_poster(self):
        await self.bot.wait_until_ready()
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    @app_commands.command(name="cybersecurity", description="Fetch latest cybersecurity news from a specific source")
    @app_commands.describe(source="News source to fetch from")
    async def cybersecurity_news(self, interaction: discord.Interaction, source: str):
        """Manually fetch news from a specific source."""
        if source not in NEWS_SOURCES:
            await interaction.response.send_message(
                f"❌ Unknown source. Use `/news list_sources cybersecurity` to see available sources.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(thinking=True)
        
        title, link, description = await self._fetch_rss_feed(source)
        
        if not title:
            await interaction.followup.send("❌ Failed to fetch news from this source.")
            return
        
        source_info = NEWS_SOURCES[source]
        
        embed = discord.Embed(
            title=f"{source_info['icon']} {title}",
            url=link,
            description=description,
            color=source_info['color'],
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Source: {source_info['name']}")
        
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CybersecurityNews(bot))
    logger.info("Cybersecurity News cog loaded")
