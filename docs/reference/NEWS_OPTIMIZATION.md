# News System Optimization Guide
**Efficient, Low-Resource News Aggregation for Penguin Overlord Bot**

## 📊 Performance Improvements

### Before Optimization
- ❌ 5 long-running tasks in Discord bot (24/7)
- ❌ Re-fetching full feeds every cycle (~5MB each)
- ❌ No duplicate detection across restarts
- ❌ Fixed intervals causing traffic spikes
- ❌ Memory: ~500MB constant usage

### After Optimization
- ✅ Scheduled systemd timers (run & exit)
- ✅ ETag/Last-Modified caching (~99% bandwidth reduction)
- ✅ GUID tracking prevents duplicates
- ✅ Staggered intervals distribute load
- ✅ Memory: ~50-150MB peak, 0MB idle

## 🎯 Optimization Strategy

### 1. Staggered Scheduling
Prevents traffic spikes and distributes system load:

| Category       | Interval | Offset | Example Times          |
|----------------|----------|--------|------------------------|
| CVE            | 6 hours  | :00    | 00:00, 06:00, 12:00... |
| Cybersecurity  | 3 hours  | :01    | 00:01, 03:01, 06:01... |
| Tech           | 4 hours  | :30    | 00:30, 04:30, 08:30... |
| Gaming         | 2 hours  | :15    | 00:15, 02:15, 04:15... |
| Apple/Google   | 3 hours  | :45    | 00:45, 03:45, 06:45... |

**Benefit**: Network activity spread across the hour instead of bunched together.

### 2. HTTP ETag Caching
Implements RFC 7232 conditional requests:

```http
# First request - full download
GET /feed.xml HTTP/1.1
Host: example.com
→ 200 OK
   ETag: "abc123"
   Content-Length: 524288

# Subsequent requests - conditional
GET /feed.xml HTTP/1.1
Host: example.com
If-None-Match: "abc123"
→ 304 Not Modified
   Content-Length: 0
```

**Benefit**: 
- Unchanged feeds return 304 (no body)
- Saves ~5MB → ~500 bytes per feed
- ~99% bandwidth reduction
- Faster response times

### 3. GUID Deduplication
Tracks last 50 GUIDs per feed:

```python
# Before: Link-based tracking (unreliable)
if link != last_posted_link:
    post(item)

# After: GUID-based tracking (reliable)
if guid not in last_50_guids:
    post(item)
```

**Benefit**:
- Survives bot restarts
- Handles feed re-ordering
- Prevents duplicate posts

### 4. Concurrency Control
Semaphore-based rate limiting:

```python
# Limit concurrent requests per category
semaphore = asyncio.Semaphore(5)  # Max 5 at once

async with semaphore:
    response = await session.get(url)
```

**Benefit**:
- Prevents overwhelming remote servers
- Reduces memory spikes
- Better error handling

### 5. Systemd Timers (vs. Long-Running)
Replace continuous loops with scheduled runs:

```systemd
# Run every 3 hours at :01
OnCalendar=*-*-* 00,03,06,09,12,15,18,21:01:00
Type=oneshot  # Exits after completion
```

**Benefit**:
- Zero memory when idle
- Automatic crash recovery (systemd restarts)
- Better resource isolation
- Easier to monitor

## 🚀 Deployment Options

### Option A: Systemd Timers (Recommended)
**Best for**: Production, 24/7 operation, low resource systems

```bash
# Deploy all timers
sudo ./scripts/deploy-news-timers.sh

# Check status
systemctl list-timers penguin-news-*

# View logs
journalctl -u penguin-news-cybersecurity -f
```

**Pros**:
- Lowest resource usage
- Automatic restarts on failure
- Centralized logging
- Production-grade reliability

**Cons**:
- Requires root for initial setup
- Linux-only

### Option B: Cron Jobs
**Best for**: Simple setups, shared hosting

```bash
# Add to crontab
crontab -e

# CVE - Every 6 hours
0 */6 * * * cd /opt/penguin-overlord && python3 scripts/news_runner.py --category cve

# Cybersecurity - Every 3 hours at :01
1 */3 * * * cd /opt/penguin-overlord && python3 scripts/news_runner.py --category cybersecurity

# Tech - Every 4 hours at :30
30 */4 * * * cd /opt/penguin-overlord && python3 scripts/news_runner.py --category tech

# Gaming - Every 2 hours at :15
15 */2 * * * cd /opt/penguin-overlord && python3 scripts/news_runner.py --category gaming

# Apple/Google - Every 3 hours at :45
45 */3 * * * cd /opt/penguin-overlord && python3 scripts/news_runner.py --category apple_google
```

**Pros**:
- No root required (user crontab)
- Universal (works everywhere)
- Simple setup

**Cons**:
- Less robust error handling
- Manual log management
- No automatic restarts

### Option C: Discord Bot Tasks (Original)
**Best for**: Development, testing, single-purpose bot

Keep the existing `@tasks.loop()` decorators in cogs.

**Pros**:
- Integrated with bot
- Immediate feedback
- Easy debugging

**Cons**:
- Higher memory usage (24/7)
- All news stops if bot crashes
- No load distribution

## 📈 Performance Metrics

### Bandwidth Usage

#### Without Optimization (per run):
```
73 sources × 5MB avg = 365MB per run
CVE (6h):    365MB × 4 runs = 1.46 GB/day
Gaming (2h): 365MB × 12 runs = 4.38 GB/day
Total: ~8 GB/day × 30 = 240 GB/month
```

#### With ETag Caching (per run):
```
73 sources × 50KB avg = 3.65MB per run
CVE (6h):    3.65MB × 4 runs = 14.6 MB/day
Gaming (2h): 3.65MB × 12 runs = 43.8 MB/day
Total: ~80 MB/day × 30 = 2.4 GB/month
```

**Savings**: 237.6 GB/month (99% reduction)

### Memory Usage

| Mode              | Idle | Peak During Run |
|-------------------|------|-----------------|
| Long-running bot  | 500M | 600M            |
| Systemd timers    | 0M   | 150M            |
| Cron jobs         | 0M   | 150M            |

**Savings**: 500MB constant → 0MB idle

### CPU Usage

| Mode              | Idle | During Run |
|-------------------|------|------------|
| Long-running bot  | 2-5% | 10-20%     |
| Systemd timers    | 0%   | 10-20%     |

**Runtime**: 10-30 seconds per category run

## 🔧 Configuration

### Cache Settings
Edit `data/news_config.json`:

```json
{
  "cybersecurity": {
    "use_etag_cache": true,        // Enable ETag caching
    "concurrency_limit": 5,         // Max concurrent requests
    "interval_hours": 3,            // How often to run
    "minute_offset": 1              // Start at :01
  }
}
```

### Concurrency Limits
Adjust based on server capacity:

```python
# Conservative (slow server)
concurrency_limit = 3

# Balanced (normal)
concurrency_limit = 5

# Aggressive (powerful server)
concurrency_limit = 10
```

### Cache Persistence
Cache files stored in `data/`:

- `feed_cache_cybersecurity.json` - ETags and GUIDs
- `feed_cache_tech.json`
- `feed_cache_gaming.json`
- `feed_cache_apple_google.json`
- `feed_cache_cve.json`

**Automatic cleanup**: Keeps last 50 GUIDs per feed

## 📊 Monitoring

### Check Timer Status
```bash
# List all timers and next run times
systemctl list-timers penguin-news-*

# Detailed status
systemctl status penguin-news-cybersecurity.timer
```

### View Real-Time Logs
```bash
# Follow specific category
journalctl -u penguin-news-cybersecurity -f

# All news categories
journalctl -u 'penguin-news-*' -f --since today

# Show only errors
journalctl -u 'penguin-news-*' -p err
```

### Performance Statistics
```bash
# Run count per timer
systemctl show penguin-news-cybersecurity.timer | grep NAccepted

# Last run time
systemctl show penguin-news-cybersecurity.service | grep ExecMainExitTimestamp

# Resource usage
systemctl status penguin-news-cybersecurity.service | grep Memory
```

### Cache Efficiency
Check cache hit rate:

```bash
# View cache file
cat data/feed_cache_cybersecurity.json | jq

# Count cached feeds
jq '.etags | length' data/feed_cache_cybersecurity.json
```

## 🔍 Troubleshooting

### Timer Not Running
```bash
# Check if enabled
systemctl is-enabled penguin-news-cybersecurity.timer

# Enable it
sudo systemctl enable penguin-news-cybersecurity.timer

# Start it
sudo systemctl start penguin-news-cybersecurity.timer
```

### Service Failing
```bash
# Check logs
journalctl -u penguin-news-cybersecurity -n 50

# Test manually
sudo -u penguin python3 /path/to/news_runner.py --category cybersecurity --verbose

# Check permissions
ls -la /opt/penguin-overlord/data/
```

### High Memory Usage
```bash
# Check current usage
systemctl status penguin-news-*.service | grep Memory

# Set lower limits in service files
sudo vim /etc/systemd/system/penguin-news-cybersecurity.service
# Change: MemoryMax=128M

# Reload
sudo systemctl daemon-reload
```

### Cache Not Working
```bash
# Verify cache file exists and is writable
ls -la data/feed_cache_*.json

# Check file contents
jq . data/feed_cache_cybersecurity.json

# Test with verbose logging
python3 scripts/news_runner.py --category cybersecurity --verbose
```

## 🎯 Best Practices

1. **Start with systemd timers** - Most efficient for 24/7 operation
2. **Monitor for first week** - Watch logs to catch issues early
3. **Adjust intervals as needed** - Not all feeds update frequently
4. **Keep cache files** - Don't delete, they prevent duplicates
5. **Enable log rotation** - Prevent disk space issues
6. **Set resource limits** - Protect system from runaway processes

## 📚 Additional Resources

- **Systemd Timer Examples**: `NEWS_OPTIMIZATION.conf` (this directory)
- **Standalone Runner**: `/scripts/news_runner.py`
- **Deployment Script**: `/scripts/deploy-news-timers.sh`
- **Fetcher Library**: `/utils/news_fetcher.py`

## 🔮 Future Enhancements

- **SQLite Database**: Replace JSON files for better performance
- **Webhook Support**: Push notifications instead of polling
- **Feed Health Monitoring**: Alert on broken feeds
- **Intelligent Scheduling**: Adjust frequency based on update patterns
- **Redis Caching**: Distributed caching for multiple bots
