# Changelog

All notable changes to Penguin Overlord will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- SOLAR_POST_CHANNEL_ID environment variable support in radiohead.py
- Comprehensive documentation index (docs/README.md)
- Organized documentation structure with 7 categories
- New help system with dropdown navigation (now as `!help`)
- General News category with 7 major news outlets
- News timer deployment mode awareness (Python vs Docker)

### Changed
- **BREAKING**: All auto-posting now defaults to DISABLED (must explicitly enable)
- **BREAKING**: Removed legacy SecurityNews system (use NEWS_CYBERSECURITY_CHANNEL_ID instead)
- **BREAKING**: `!help` now uses new dropdown system (old paginated help available as `!help_old`)
- Merged `!propagation` command into `!solar` (propagation now an alias)
- News timers now match bot deployment mode (Python venv or Docker containers)
- Reorganized documentation into structured folders:
  - setup/ - Getting started guides
  - features/ - Feature documentation
  - deployment/ - Production deployment
  - secrets/ - Secrets management
  - reference/ - Technical references
  - migration/ - Upgrade guides
  - archive/ - Historical documents
- Updated README.md with documentation navigation section
- Consolidated Doppler documentation

### Deprecated
- `!propagation` command (use `!solar` instead - propagation is now an alias)
- SECNEWS_POST_CHANNEL_ID environment variable (use NEWS_CYBERSECURITY_CHANNEL_ID)

### Removed
- securitynews.py cog (replaced by cybersecurity_news.py in News System)
- Duplicate/redundant documentation files

### Fixed
- UK Legislation Tracker RSS feed parsing to handle `<item>` tags with attributes (e.g., `rdf:about`)
- Inconsistent default behavior (XKCD and Comics now disabled by default like News)
- Documentation scattered across project root (now organized in docs/)

## [1.0.0] - 2025-11-09

### Added
- News aggregation system with 90 sources across 8 categories
- Cybersecurity news (18 sources)
- Technology news (15 sources)
- Gaming news (10 sources)
- Apple & Google news (27 sources)
- CVE vulnerability tracking (3 sources)
- US Legislation tracking (5 government sources)
- EU Legislation tracking (3 official sources)
- General news outlets (7 major sources)
- Date filtering to prevent historical spam
- ETag caching for efficient RSS fetching
- Concurrent fetching with configurable limits
- Per-source enable/disable control
- Environment variable support for all news channels

### Changed
- News system now uses modern architecture with dedicated category cogs
- All RSS feeds verified and tested (HTTP 200 OK)
- NO API keys required - all feeds are public

---

## Upgrade Guide

### From Previous Version → Latest

#### 1. Update Environment Variables
```bash
# Old (if using legacy security news)
SECNEWS_POST_CHANNEL_ID=123456789

# New (recommended)
NEWS_CYBERSECURITY_CHANNEL_ID=123456789
```

#### 2. Re-enable Auto-Posting
After upgrading, all auto-posting will be disabled. Re-enable as needed:

```bash
# XKCD
!xkcd_enable

# Comics
!comic_enable

# Solar
!solar_enable

# News (each category separately)
/news enable cybersecurity
/news enable tech
# ... etc
```

#### 3. Update Commands
- Change `!propagation` → `!solar` (or keep using propagation as alias)
- Change `!secnews_*` → `/news` commands

#### 4. Update Documentation Links
If you have custom documentation pointing to old files:
- Update paths to new docs/ structure
- Check [docs/README.md](docs/README.md) for new locations

---

## Documentation Changes

### File Moves

**Root → docs/setup/**
- GET_DISCORD_TOKEN.md → docs/setup/DISCORD_SETUP.md
- DISCORD_PERMISSIONS.md → docs/setup/PERMISSIONS.md

**Root → docs/deployment/**
- DEPLOYMENT.md → docs/deployment/PRODUCTION.md
- docs/SYSTEMD_INSTALL_GUIDE.md → docs/deployment/SYSTEMD.md

**Root → docs/secrets/**
- SECRETS_QUICK_REFERENCE.md → docs/secrets/README.md

**Root → docs/features/**
- NEWS_SYSTEM_SUMMARY.md → docs/features/NEWS_SYSTEM.md

**docs/ → docs/reference/**
- CHANNEL_CONFIGURATION_REFERENCE.md → docs/reference/CHANNEL_CONFIGURATION.md
- RSS_FEEDS_AND_API_KEYS.md → docs/reference/RSS_FEEDS.md
- NEWS_OPTIMIZATION_GUIDE.md → docs/reference/NEWS_OPTIMIZATION.md
- HELP_SYSTEM_GUIDE.md → docs/reference/HELP_SYSTEM.md

**docs/ → docs/migration/**
- NOVEMBER_2025_BREAKING_CHANGES.md → docs/migration/NOVEMBER_2025_BREAKING_CHANGES.md

**docs/ → docs/archive/** (Historical)
- DOPPLER_INTEGRATION.md
- DOPPLER_SETUP.md
- HOUSEKEEPING_NOVEMBER_2025.md
- NEWS_CATEGORY_REORGANIZATION.md
- LEGISLATION_FEED_UPDATES.md
- LEGISLATION_DATE_FILTERING.md
- LEGISLATION_TRACKING.md
- US_LEGISLATION_SOURCES.md
- TEST_RESULTS.md

### New Documentation
- docs/README.md - Complete documentation index
- CHANGELOG.md - This file

---

## Statistics

### Before Cleanup
- **Root-level docs**: 10 files
- **docs/ structure**: Flat, 13 files
- **Total docs**: 23 files
- **Documentation index**: None
- **Duplicate docs**: 6

### After Cleanup
- **Root-level docs**: 2 files (README.md, QUICK_REFERENCE.md)
- **docs/ structure**: 7 organized directories
- **Total docs**: 24 files (1 new: CHANGELOG.md)
- **Documentation index**: Complete with navigation
- **Duplicate docs**: 0 (consolidated)
- **Archive docs**: 9 (preserved history)

### Code Changes
- **Cogs modified**: 3 (xkcd_poster.py, comics.py, radiohead.py)
- **Cogs deprecated**: 1 (securitynews.py)
- **Lines changed**: ~50 lines
- **Breaking changes**: 2 (auto-posting defaults, legacy removal)
- **Backward compatibility**: High (aliases and migration guides provided)

---

## Contributors

- ChiefGyk3D - Project maintainer and primary developer

---

## License

This project is licensed under the Mozilla Public License 2.0 - see the LICENSE file for details.

---

**For detailed migration instructions, see [docs/migration/NOVEMBER_2025_BREAKING_CHANGES.md](docs/migration/NOVEMBER_2025_BREAKING_CHANGES.md)**
