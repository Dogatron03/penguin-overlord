# News Categories Overview

## Complete Category Structure

```
📰 PENGUIN OVERLORD NEWS SYSTEM
├── 🔒 Cybersecurity (18 sources, every 3h at :01)
├── 💻 Tech (15 sources, every 4h at :30)
├── 🎮 Gaming (10 sources, every 2h at :15)
├── 🍎 Apple/Google (27 sources, every 3h at :45)
├── 🛡️ CVE (3 sources, every 6h at :00)
├── 🏛️ US Legislation (5 sources, hourly at :05)
│   ├── ✍️ Bills Presented to President
│   ├── 🏛️ House Floor Today
│   ├── 🏛️ Senate Floor Today
│   ├── 📋 Most Viewed Bills
│   └── 📜 GovInfo Bills
├── 🇪🇺 EU Legislation (3 sources, hourly at :10)
│   ├── 🇪🇺 EUR-Lex Legislation
│   ├── 🏛️ European Parliament News
│   └── 📰 Council of EU Press
└── 🌍 General News (7 sources, every 2h at :20) ✨ NEW
    ├── 📻 NPR News
    ├── 📺 PBS NewsHour - Economy
    ├── 💼 Financial Times
    ├── 📊 Pew Research Center
    ├── 📰 New York Times
    ├── 🌍 Foreign Affairs
    └── 🏛️ Politico

Total: 90 sources across 8 categories
```

## Quick Reference

### Discord Commands

```bash
# Cybersecurity
/cybersecuritynews <source>

# Tech
/technews <source>

# Gaming
/gamingnews <source>

# Apple/Google
/applegooglenews <source>

# CVE
/cve <source>

# US Legislation (5 govt sources only)
/uslegislation <source>

# EU Legislation
/eulegislation <source>

# General News (7 news outlets) ✨ NEW
/generalnews <source>
```

### Configuration

```bash
# Via Discord
/news set_channel <category> #channel
/news enable <category>
/news disable <category>
/news toggle_source <category> <source>

# Via Environment Variables
NEWS_CYBERSECURITY_CHANNEL_ID=111...
NEWS_TECH_CHANNEL_ID=222...
NEWS_GAMING_CHANNEL_ID=333...
NEWS_APPLE_GOOGLE_CHANNEL_ID=444...
NEWS_CVE_CHANNEL_ID=555...
NEWS_US_LEGISLATION_CHANNEL_ID=666...
NEWS_EU_LEGISLATION_CHANNEL_ID=777...
NEWS_GENERAL_NEWS_CHANNEL_ID=888...  # NEW
```

## Key Features

- ✅ **No API Keys Required** - All 90 feeds are public RSS
- ✅ **Error Handling** - Failed feeds don't crash the bot
- ✅ **Date Filtering** - Only posts content from last 7 days
- ✅ **Deduplication** - Never posts the same item twice
- ✅ **Staggered Updates** - No overlapping category runs
- ✅ **Rate Limiting** - 2-second delays between sources
- ✅ **Configurable** - Enable/disable categories and sources
- ✅ **Flexible** - Configure via .env, Doppler, or Discord commands

## Update Schedule

```
Time    Category              Frequency
────────────────────────────────────────
:00     CVE                  Every 6 hours
:01     Cybersecurity        Every 3 hours
:05     US Legislation       Every hour
:10     EU Legislation       Every hour
:15     Gaming               Every 2 hours
:20     General News ✨      Every 2 hours
:30     Tech                 Every 4 hours
:45     Apple/Google         Every 3 hours
```

All times are minute offsets (e.g., :05 = 00:05, 01:05, 02:05...)

## Source Breakdown

| Category | Official Govt | News Media | Tech Blogs | Research | Total |
|----------|--------------|------------|------------|----------|-------|
| Cybersecurity | 2 | 8 | 8 | 0 | **18** |
| Tech | 0 | 7 | 8 | 0 | **15** |
| Gaming | 0 | 5 | 5 | 0 | **10** |
| Apple/Google | 0 | 12 | 15 | 0 | **27** |
| CVE | 3 | 0 | 0 | 0 | **3** |
| US Legislation | 5 | 0 | 0 | 0 | **5** |
| EU Legislation | 3 | 0 | 0 | 0 | **3** |
| General News | 0 | 6 | 0 | 1 | **7** |
| **TOTAL** | **13** | **38** | **36** | **1** | **90** |

## What's New (Nov 9, 2025)

### Added ✨
- **General News category** with 7 sources
- **Financial Times** feed (corrected URL)
- **Environment variable support** for channel IDs

### Fixed 🔧
- Removed broken feeds (Congress most-recent-bills, C-SPAN, AP News)
- Financial Times URL corrected to proper RSS endpoint
- US Legislation now contains only government sources

### Reorganized 🗂️
- Moved 6 news outlets from US Legislation to General News
- Proper separation: government sources vs. news media
- Clear categorization for users

## Status: Production Ready ✅

All 90 feeds tested and working. No API keys required. Ready to deploy!
