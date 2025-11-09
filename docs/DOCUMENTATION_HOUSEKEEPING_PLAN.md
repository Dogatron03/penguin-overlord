# Documentation Housekeeping Plan - November 2025

## Overview

Consolidate and organize documentation, add Penguin Overlord branding, remove redundancy.

## Current State Analysis

### Root-Level Documentation (24 files)
```
/home/chiefgyk3d/src/penguin-overlord/
├── README.md                          [KEEP - Main entry point]
├── DEPLOYMENT.md                      [CONSOLIDATE → docs/]
├── DISCORD_PERMISSIONS.md             [CONSOLIDATE → docs/]
├── DOPPLER_INTEGRATION.md             [CONSOLIDATE → docs/secrets/]
├── DOPPLER_SETUP.md                   [CONSOLIDATE → docs/secrets/]
├── GET_DISCORD_TOKEN.md               [CONSOLIDATE → docs/setup/]
├── NEWS_SYSTEM_SUMMARY.md             [CONSOLIDATE → docs/features/]
├── QUICK_REFERENCE.md                 [KEEP - Quick access]
├── SECRETS_QUICK_REFERENCE.md         [CONSOLIDATE → docs/secrets/]
└── TEST_RESULTS.md                    [ARCHIVE → tests/]
```

### docs/ Directory (13 files)
```
docs/
├── CHANNEL_CONFIGURATION_REFERENCE.md [KEEP - Current, comprehensive]
├── HELP_SYSTEM_GUIDE.md              [KEEP - Current]
├── HOUSEKEEPING_NOVEMBER_2025.md     [ARCHIVE - Historical]
├── NOVEMBER_2025_BREAKING_CHANGES.md [KEEP - Important]
├── NEWS_CATEGORIES_OVERVIEW.md       [KEEP - Good overview]
├── NEWS_CATEGORY_REORGANIZATION.md   [ARCHIVE - Historical]
├── NEWS_OPTIMIZATION_GUIDE.md        [KEEP - Technical guide]
├── RSS_FEEDS_AND_API_KEYS.md         [KEEP - Important reference]
├── SYSTEMD_INSTALL_GUIDE.md          [MOVE → docs/deployment/]
├── LEGISLATION_DATE_FILTERING.md     [CONSOLIDATE → NEWS_CATEGORIES_OVERVIEW]
├── LEGISLATION_FEED_UPDATES.md       [ARCHIVE - Historical]
├── LEGISLATION_TRACKING.md           [CONSOLIDATE → NEWS_CATEGORIES_OVERVIEW]
└── US_LEGISLATION_SOURCES.md         [CONSOLIDATE → NEWS_CATEGORIES_OVERVIEW]
```

## Proposed New Structure

```
/home/chiefgyk3d/src/penguin-overlord/
│
├── README.md                          # Main - with Penguin banner
├── QUICK_REFERENCE.md                 # Quick command reference
├── CHANGELOG.md                       # NEW - Track all changes
│
├── docs/
│   ├── README.md                      # NEW - Documentation index
│   │
│   ├── setup/                         # NEW - Getting started
│   │   ├── INSTALLATION.md            # NEW - Combined setup guide
│   │   ├── DISCORD_SETUP.md           # From GET_DISCORD_TOKEN.md
│   │   ├── PERMISSIONS.md             # From DISCORD_PERMISSIONS.md
│   │   └── CONFIGURATION.md           # NEW - Basic config guide
│   │
│   ├── features/                      # NEW - Feature documentation
│   │   ├── NEWS_SYSTEM.md             # Combined news docs
│   │   ├── HAM_RADIO.md               # NEW - Solar/propagation
│   │   ├── COMICS.md                  # NEW - XKCD + daily comics
│   │   ├── AVIATION.md                # NEW - Planespotter
│   │   ├── EVENTS.md                  # NEW - EventPinger
│   │   └── UTILITIES.md               # NEW - Fortune, manpages, etc.
│   │
│   ├── deployment/                    # Deployment guides
│   │   ├── SYSTEMD.md                 # From SYSTEMD_INSTALL_GUIDE.md
│   │   ├── DOCKER.md                  # NEW - Docker deployment
│   │   └── PRODUCTION.md              # From DEPLOYMENT.md
│   │
│   ├── secrets/                       # Secrets management
│   │   ├── README.md                  # NEW - Secrets overview
│   │   ├── DOPPLER.md                 # Merge DOPPLER_*.md
│   │   ├── AWS.md                     # NEW - AWS Secrets Manager
│   │   └── VAULT.md                   # NEW - HashiCorp Vault
│   │
│   ├── reference/                     # Technical references
│   │   ├── CHANNEL_CONFIGURATION.md   # From CHANNEL_CONFIGURATION_REFERENCE.md
│   │   ├── RSS_FEEDS.md               # From RSS_FEEDS_AND_API_KEYS.md
│   │   ├── NEWS_OPTIMIZATION.md       # From NEWS_OPTIMIZATION_GUIDE.md
│   │   └── HELP_SYSTEM.md             # From HELP_SYSTEM_GUIDE.md
│   │
│   ├── migration/                     # Migration guides
│   │   └── NOVEMBER_2025.md           # From NOVEMBER_2025_BREAKING_CHANGES.md
│   │
│   └── archive/                       # Historical documents
│       ├── HOUSEKEEPING_NOVEMBER_2025.md
│       ├── NEWS_CATEGORY_REORGANIZATION.md
│       ├── LEGISLATION_FEED_UPDATES.md
│       └── TEST_RESULTS.md
│
└── tests/
    └── README.md                      # Test documentation
```

## Action Items

### Phase 1: Branding (Priority: High)
- [ ] Create Penguin Overlord ASCII art banner
- [ ] Add banner to README.md
- [ ] Add banner to docs/README.md
- [ ] Add banner to QUICK_REFERENCE.md
- [ ] Update all docs with consistent header format

### Phase 2: Consolidation (Priority: High)
- [ ] Merge Doppler docs: DOPPLER_INTEGRATION.md + DOPPLER_SETUP.md → docs/secrets/DOPPLER.md
- [ ] Merge Legislation docs into docs/features/NEWS_SYSTEM.md:
  - LEGISLATION_DATE_FILTERING.md
  - LEGISLATION_TRACKING.md
  - US_LEGISLATION_SOURCES.md
- [ ] Move SYSTEMD_INSTALL_GUIDE.md → docs/deployment/SYSTEMD.md
- [ ] Move GET_DISCORD_TOKEN.md → docs/setup/DISCORD_SETUP.md
- [ ] Move DISCORD_PERMISSIONS.md → docs/setup/PERMISSIONS.md

### Phase 3: New Documentation (Priority: Medium)
- [ ] Create docs/README.md - Documentation index with links
- [ ] Create CHANGELOG.md - Track all changes going forward
- [ ] Create docs/setup/INSTALLATION.md - Step-by-step setup
- [ ] Create docs/features/HAM_RADIO.md - Solar/propagation features
- [ ] Create docs/features/COMICS.md - XKCD + daily comics
- [ ] Create docs/deployment/DOCKER.md - Docker deployment guide

### Phase 4: Archival (Priority: Low)
- [ ] Move historical docs to docs/archive/:
  - HOUSEKEEPING_NOVEMBER_2025.md
  - NEWS_CATEGORY_REORGANIZATION.md
  - LEGISLATION_FEED_UPDATES.md
  - TEST_RESULTS.md
- [ ] Update all links to archived docs
- [ ] Add note to archived docs: "Archived for historical reference"

### Phase 5: Code Changes (Priority: High)
- [ ] Merge `!propagation` into `!solar` (make propagation an alias)
- [ ] Add SOLAR_POST_CHANNEL_ID env var support to radiohead.py
- [ ] Update help text to reflect consolidated commands
- [ ] Update cog descriptions

## Banner Design

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   ██████╗ ███████╗███╗   ██╗ ██████╗ ██╗   ██╗██╗███╗   ██╗           ║
║   ██╔══██╗██╔════╝████╗  ██║██╔════╝ ██║   ██║██║████╗  ██║           ║
║   ██████╔╝█████╗  ██╔██╗ ██║██║  ███╗██║   ██║██║██╔██╗ ██║           ║
║   ██╔═══╝ ██╔══╝  ██║╚██╗██║██║   ██║██║   ██║██║██║╚██╗██║           ║
║   ██║     ███████╗██║ ╚████║╚██████╔╝╚██████╔╝██║██║ ╚████║           ║
║   ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝           ║
║                                                                          ║
║    ██████╗ ██╗   ██╗███████╗██████╗ ██╗      ██████╗ ██████╗ ██████╗  ║
║   ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗ ║
║   ██║   ██║██║   ██║█████╗  ██████╔╝██║     ██║   ██║██████╔╝██║  ██║ ║
║   ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██╗██║  ██║ ║
║   ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████╗╚██████╔╝██║  ██║██████╔╝ ║
║    ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  ║
║                                                                          ║
║                   🐧 Discord Bot for Hackers & Hams                     ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

Alternative simpler banner:
```
    ____                        _          ____                  __               __
   / __ \___  ____  ____ ___  __(_)___     / __ \_   _____  _____/ /___  _________/ /
  / /_/ / _ \/ __ \/ __ `/ / / / / __ \   / / / / | / / _ \/ ___/ / __ \/ ___/ __  / 
 / ____/  __/ / / / /_/ / /_/ / / / / /  / /_/ /| |/ /  __/ /  / / /_/ / /  / /_/ /  
/_/    \___/_/ /_/\__, /\__,_/_/_/ /_/   \____/ |___/\___/_/  /_/\____/_/   \__,_/   
                 /____/                                                               
                      🐧 Discord Bot for Hackers & Hams 🐧
```

## Documentation Standards

All new/updated docs should follow this format:

```markdown
# [Document Title]

> **Penguin Overlord** | [Category] | Last Updated: [Date]

[Brief description of what this document covers]

## Table of Contents
- [Section 1]
- [Section 2]
- ...

## Content

...

---

**Related Documentation:**
- [Link to related doc 1]
- [Link to related doc 2]

**Need Help?**
- Discord: Use `!help2` or `/help2`
- Issues: [GitHub Issues](https://github.com/ChiefGyk3D/penguin-overlord/issues)

---

<div align="center">
  <strong>🐧 Made with ❤️ by the Penguin Overlord Team</strong>
</div>
```

## Benefits

### User Benefits
✅ Easier to find documentation  
✅ Clear separation of setup vs reference vs features  
✅ Consistent branding and formatting  
✅ Less confusion from duplicate/outdated docs  

### Developer Benefits
✅ Easier to maintain documentation  
✅ Clear place for new docs  
✅ Historical context preserved in archive  
✅ Reduced clutter in project root  

### SEO Benefits
✅ Better organized for documentation sites  
✅ Clear hierarchy and structure  
✅ Consistent metadata and headers  

## Timeline

### Week 1 (Nov 9-15, 2025)
- Phase 1: Branding
- Phase 5: Code Changes (solar/propagation merge)

### Week 2 (Nov 16-22, 2025)
- Phase 2: Consolidation

### Week 3 (Nov 23-29, 2025)
- Phase 3: New Documentation

### Week 4 (Nov 30-Dec 6, 2025)
- Phase 4: Archival
- Final review and link updates

## Metrics

Track progress:
- [ ] Root-level docs reduced from 10 to 3
- [ ] Duplicate docs eliminated: 6 → 0
- [ ] New organized structure: 0 → 6 directories
- [ ] Banner added to: 0 → 20+ files
- [ ] Broken links fixed: TBD → 0

## Notes

- Keep all Git history intact
- Use `git mv` for file moves to preserve history
- Update all internal links after moves
- Test all links before considering complete
- Get user feedback before archiving anything

---

**Priority Order:**
1. Branding + Code Changes (Week 1)
2. Consolidation (Week 2)
3. New Docs (Week 3)
4. Archival (Week 4)
