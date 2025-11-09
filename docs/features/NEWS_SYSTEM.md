# Modular News System - Implementation Summary

## Overview
Restructured the bot's news aggregation into **5 separate categories** with centralized role-based management.

## Architecture

### 1. News Manager (news_manager.py)
**Central configuration hub** for all news categories.

**Commands:**
- `/news set_channel <category> <channel>` - Set posting channel
- `/news enable <category>` - Enable auto-posting (admin only)
- `/news disable <category>` - Disable auto-posting (admin only)
- `/news set_interval <category> <hours>` - Set posting frequency (1-24 hours)
- `/news toggle_source <category> <source>` - Enable/disable individual sources
- `/news add_role <category> <role>` - Grant role permission to manage sources
- `/news remove_role <category> <role>` - Remove role permissions
- `/news status <category>` - View current configuration
- `/news list_sources <category>` - List all available sources

**Categories:** `cybersecurity`, `tech`, `gaming`, `apple_google`, `cve`

### 2. Cybersecurity News (cybersecurity_news.py)
**18 security and threat intelligence sources**

Sources include:
- 404 Media, Ars Technica Security, The Hacker News
- WeLiveSecurity (ESET), Dark Reading, BleepingComputer
- Malwarebytes Labs, Wired Security, EFF Deeplinks
- Schneier on Security, CyberScoop, SecurityWeek
- DataBreaches.net, AWS Security Blog, CrowdStrike
- Tenable, Zscaler Research, Privacy International

**Command:** `/cybersecurity <source>` - Manual fetch from specific source

### 3. Tech News (tech_news.py)
**15 general technology and developer news sources**

Sources include:
- Ars Technica (Main), The Verge, TechCrunch, Engadget
- Phoronix (Linux/Hardware), LWN.net, Hackaday
- IEEE Spectrum, Tom's Hardware, AnandTech
- InfoQ, GitHub Blog, Google Developers Blog
- Cloudflare Engineering, VentureBeat (AI/Tech)

**Command:** `/tech <source>` - Manual fetch from specific source

### 4. Gaming News (gaming_news.py)
**10 gaming industry news sources**

Sources include:
- IGN, Game Informer, Polygon, PC Gamer
- Eurogamer, Rock Paper Shotgun, GameSpot
- Kotaku, Destructoid, Niche Gamer

**Command:** `/gaming <source>` - Manual fetch from specific source

### 5. Apple/Google News (apple_google_news.py)
**27 Apple and Google/Android ecosystem sources**

**Apple Sources (11):**
- 9to5Mac, MacRumors, AppleInsider, Cult of Mac
- MacWorld, MacStories, iMore, The Mac Observer
- TidBITS, Patently Apple, 9to5Toys (Apple Gear)

**Google/Android Sources (16):**
- 9to5Google, Android Authority, Android Police, XDA Developers
- Android Central, Droid Life, SamMobile, GSMArena
- Android Headlines, Pocketnow, Chrome Unboxed
- Google Cloud Blog, Google Workspace Updates
- Android Developers Blog, Google Developers Blog
- 9to5Toys (Google/Android Gear)

**Command:** `/applegoogle <source>` - Manual fetch from specific source

### 6. CVE News (cve.py - UPDATED)
**3 CVE tracking sources** - Now integrated with NewsManager

Sources include:
- CISA Known Exploited Vulnerabilities (JSON API)
- NVD Recent CVEs (JSON API with CVSS scoring)
- Ubuntu Security Notices (RSS)

Features:
- Severity indicators: 🔴 Critical, 🟠 High, 🟡 Medium, 🟢 Low
- Tracks last 1000 posted CVEs to prevent duplicates
- Dynamically adjusts posting interval

**Command:** `/cve <source>` - Manual fetch from specific source

## Key Features

### Role-Based Permissions
- **Administrators**: Full control over all settings
- **Approved Roles**: Can toggle individual sources on/off per category
- **Everyone**: Can view status and manually fetch news

### Per-Source Control
Each news source can be individually enabled/disabled:
```
/news toggle_source cybersecurity bleepingcomputer
```

### Separate Channels
Each category posts to its own configurable channel:
```
/news set_channel cybersecurity #security-news
/news set_channel tech #tech-news
/news set_channel gaming #gaming-news
/news set_channel apple_google #apple-google-news
/news set_channel cve #security-alerts
```

### Dynamic Intervals
Posting frequency adjustable per category (1-24 hours):
```
/news set_interval cybersecurity 4   # Every 4 hours
/news set_interval tech 6            # Every 6 hours
/news set_interval gaming 12         # Every 12 hours
```

### Duplicate Prevention
Each category tracks posted links/CVE IDs to avoid reposting:
- News cogs: Track last posted link per source
- CVE: Tracks last 1000 CVE IDs across all sources

## State Files

Configuration stored in:
- `data/news_config.json` - Central NewsManager config
- `data/cybersecurity_news_state.json`
- `data/tech_news_state.json`
- `data/gaming_news_state.json`
- `data/apple_google_news_state.json`
- `data/cve_state.json`

## Total Sources
- **Cybersecurity**: 18 sources
- **Tech**: 15 sources
- **Gaming**: 10 sources
- **Apple/Google**: 27 sources
- **CVE**: 3 sources
- **TOTAL**: **73 news sources**

## Setup Guide

1. **Set channels for each category:**
   ```
   /news set_channel cybersecurity #security-news
   /news set_channel tech #tech-news
   /news set_channel gaming #gaming-news
   /news set_channel apple_google #apple-google-news
   /news set_channel cve #security-alerts
   ```

2. **Configure posting intervals (optional):**
   ```
   /news set_interval cybersecurity 4
   /news set_interval tech 6
   /news set_interval gaming 6
   /news set_interval apple_google 6
   /news set_interval cve 6
   ```

3. **Add approved roles for source management (optional):**
   ```
   /news add_role cybersecurity @Security-Team
   /news add_role tech @Tech-Leads
   /news add_role gaming @Gaming-Moderators
   ```

4. **Enable auto-posting (admin only):**
   ```
   /news enable cybersecurity
   /news enable tech
   /news enable gaming
   /news enable apple_google
   /news enable cve
   ```

5. **Disable unwanted sources (optional):**
   ```
   /news list_sources tech
   /news toggle_source tech venturebeat
   ```

## Migration Notes

- Old `securitynews.py` remains for backward compatibility
- Old `cve.py` updated to integrate with NewsManager
- All new cogs automatically create state files on first run
- No data migration needed - fresh start for all news categories

## Testing

All cogs loaded successfully:
```
✓ News Manager cog loaded
✓ Cybersecurity News cog loaded
✓ Tech News cog loaded
✓ Gaming News cog loaded
✓ Apple/Google News cog loaded
✓ CVE News cog loaded
```

## Future Enhancements

Potential additions:
- Per-source posting cooldowns
- Source priority/weighting system
- Keyword filtering/alerting
- Webhook support for external systems
- RSS feed health monitoring
- Source performance analytics
