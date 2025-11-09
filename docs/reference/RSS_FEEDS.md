# RSS Feeds and API Keys Guide

## TL;DR - No API Keys Required! 🎉

**All RSS feeds used by Penguin Overlord are publicly accessible and require NO authentication or API keys.**

You can start tracking news and legislation immediately after configuring channel IDs.

---

## RSS vs API Access

### RSS Feeds (What We Use)
- ✅ **Public and free** - No registration required
- ✅ **No rate limits** (for reasonable use)
- ✅ **No API keys needed**
- ✅ **Simple XML format**
- ⚠️ **Limited data** - Usually just recent items
- ⚠️ **No historical search**

### API Access (What We Don't Use)
- ❌ **Requires registration** and API key
- ❌ **Rate limited** (often 1,000 requests/day)
- ❌ **More complex** authentication
- ✅ **Full data access**
- ✅ **Advanced search** and filtering
- ✅ **Historical data**

---

## Feed Status by Category

### ✅ Working Feeds (No Issues)

#### US Legislation (6 sources)
| Source | URL | Status | Notes |
|--------|-----|--------|-------|
| Bills Presented to President | congress.gov | 200 OK | Low volume |
| House Floor Today | congress.gov | 200 OK | Active during session |
| Senate Floor Today | congress.gov | 200 OK | Active during session |
| Most Viewed Bills | congress.gov | 200 OK | Public interest tracking |
| GovInfo Bills | govinfo.gov | 200 OK | **High volume** (100+ items) |
| NPR News | npr.org | 200 OK | General news |
| PBS NewsHour Economy | pbs.org | 200 OK | Economic focus |
| Pew Research | pewresearch.org | 200 OK | Research & polling |
| NYT Homepage | nytimes.com | 200 OK | General news |
| Foreign Affairs | foreignaffairs.com | 200 OK | International policy |
| Politico | politico.com | 200 OK | Political news |

#### EU Legislation (3 sources)
| Source | URL | Status | Notes |
|--------|-----|--------|-------|
| EUR-Lex | europa.eu | 200 OK | Official EU law |
| European Parliament | europarl.europa.eu | 200 OK | Parliament news |
| Council of EU | consilium.europa.eu | 200 OK | Council press releases |

#### News Categories (73 sources)
All cybersecurity, tech, gaming, Apple/Google, and CVE feeds are working with 200 OK status.

### ❌ Removed Feeds (Broken)

These feeds returned errors and have been removed:

| Feed | URL | Status | Issue |
|------|-----|--------|-------|
| Congress Most Recent Bills | congress.gov | 404 | Not found |
| C-SPAN Executive | c-span.org | 410 | Gone (discontinued) |
| AP Politics | apnews.com | 404 | Not found |

### ⚠️ Redirected Feeds

| Feed | URL | Status | Notes |
|------|-----|--------|-------|
| Reuters Politics | reutersagency.com | 301 | Permanent redirect - aiohttp handles automatically |
| Financial Times | ft.com | 301 | May require subscription for full content |

---

## Error Handling

### Built-in Protections

All news and legislation cogs include comprehensive error handling:

```python
# HTTP Status Checks
if response.status != 200:
    logger.warning(f"{source['name']}: HTTP {response.status}")
    return None

# Timeout Protection
timeout = aiohttp.ClientTimeout(total=10, connect=5)

# Exception Handling
try:
    async with self.session.get(source['url']) as response:
        # ... fetch and parse ...
except asyncio.TimeoutError:
    logger.warning(f"{source['name']}: Request timeout")
    return None
except Exception as e:
    logger.error(f"{source['name']}: Error: {e}")
    return None
```

### What Happens When a Feed Fails

1. **HTTP Error (404, 500, etc.)** → Logs warning, skips to next source
2. **Timeout** → Logs warning, skips after 10 seconds
3. **Parse Error** → Logs error, skips source
4. **Network Error** → Logs error, retries on next scheduled run

**Important:** Failed feeds don't crash the bot or stop other sources from working!

### Monitoring Feed Health

Check logs to see feed status:

```bash
# View recent news feed activity
journalctl -u penguin-news-cybersecurity -n 100

# Watch for errors in real-time
journalctl -u penguin-news-us_legislation -f | grep -E "ERROR|WARNING"

# Check all news services
systemctl status 'penguin-news-*'
```

Look for patterns like:
- ✅ `"Posted: <title>"` - Successfully fetched and posted
- ⚠️ `"HTTP 404"` - Feed not found
- ⚠️ `"Request timeout"` - Feed too slow
- ⚠️ `"No items found"` - Feed empty (may be normal during recess)

---

## GovInfo Special Case

### GovInfo Bills Feed

**URL:** `https://www.govinfo.gov/rss/bills.xml`
**Status:** ✅ Working (no API key needed)
**Volume:** Very high (100+ items)

#### Important Notes

1. **RSS Feed is Public**
   - No API key required for RSS access
   - Same content as on their website
   - Updated regularly

2. **API is Separate**
   - GovInfo has an API at `api.govinfo.gov`
   - API requires key for advanced features
   - We don't use the API - only RSS

3. **Date Filtering Helps**
   - Our 7-day filter prevents spam
   - Still may post 5-10 items per hour
   - Consider disabling if too noisy:
     ```
     /news toggle_source us_legislation govinfo_bills
     ```

---

## Testing Feeds Yourself

### Quick HTTP Status Check

```bash
# Test a single feed
curl -I https://www.govinfo.gov/rss/bills.xml

# Batch test multiple feeds
for url in \
  "https://www.congress.gov/rss/presented-to-president.xml" \
  "https://www.govinfo.gov/rss/bills.xml" \
  "https://feeds.npr.org/1001/rss.xml"; do
  echo -n "$(basename $url): "
  curl -s -o /dev/null -w "%{http_code}\n" --max-time 5 "$url"
done
```

Expected: `200` = Working, `404` = Not found, `301/302` = Redirect

### Verify RSS Content

```bash
# Download and inspect feed
curl -s https://feeds.npr.org/1001/rss.xml | head -50

# Count items in feed
curl -s https://www.govinfo.gov/rss/bills.xml | grep -c "<item>"
```

### Test from Python

```python
import aiohttp
import asyncio

async def test_feed(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            print(f"{url}: {resp.status}")
            if resp.status == 200:
                content = await resp.text()
                print(f"  Length: {len(content)} bytes")

asyncio.run(test_feed("https://feeds.npr.org/1001/rss.xml"))
```

---

## Configuration with Environment Variables

### Setting Channel IDs

You can configure channel IDs via `.env` or Doppler:

```bash
# .env file
NEWS_CYBERSECURITY_CHANNEL_ID=123456789012345678
NEWS_TECH_CHANNEL_ID=234567890123456789
NEWS_GAMING_CHANNEL_ID=345678901234567890
NEWS_APPLE_GOOGLE_CHANNEL_ID=456789012345678901
NEWS_CVE_CHANNEL_ID=567890123456789012
NEWS_US_LEGISLATION_CHANNEL_ID=678901234567890123
NEWS_EU_LEGISLATION_CHANNEL_ID=789012345678901234
```

### Doppler Configuration

```bash
# Set in Doppler
doppler secrets set NEWS_US_LEGISLATION_CHANNEL_ID="123456789012345678"
doppler secrets set NEWS_EU_LEGISLATION_CHANNEL_ID="234567890123456789"
```

### Discord Commands (Alternative)

You can also configure via Discord:

```
/news set_channel us_legislation #us-legislation
/news set_channel eu_legislation #eu-legislation
/news enable us_legislation
/news enable eu_legislation
```

---

## Adding New Feeds

### Requirements

1. **Must be RSS or Atom format**
   - Check for `<rss>`, `<feed>`, or `<channel>` tags
   - Must contain `<item>` or `<entry>` elements

2. **Must be publicly accessible**
   - No authentication required
   - Returns HTTP 200
   - No paywall for RSS content

3. **Must have reasonable volume**
   - Ideally < 50 items per day
   - Use date filtering for high-volume feeds

### Adding to a Category

1. **Edit the source file** (e.g., `cogs/us_legislation.py`):

```python
LEGISLATION_SOURCES = {
    # ... existing sources ...
    'new_source': {
        'name': 'New Source Name',
        'url': 'https://example.com/feed.xml',
        'emoji': '📰'
    }
}
```

2. **Update the command Literal**:

```python
source: Literal['existing', 'sources', 'new_source']
```

3. **Test the feed**:

```bash
curl -I https://example.com/feed.xml
# Expect: HTTP/2 200
```

4. **Test in Discord**:

```
/uslegislation new_source
```

### Feed Validation Checklist

- [ ] Feed returns HTTP 200
- [ ] Content is valid XML
- [ ] Contains `<item>` or `<entry>` tags
- [ ] Items have `<title>` and `<link>`
- [ ] Items have publication date (`<pubDate>`, `<published>`)
- [ ] Feed updates regularly (check timestamps)
- [ ] No authentication required
- [ ] Volume is reasonable (< 100 items/day)

---

## Troubleshooting

### "No items found" but feed exists

**Causes:**
- Feed is empty (common during congressional recess)
- All items are older than 7 days (date filtered)
- All items already posted (deduplication)

**Solution:** Normal behavior, wait for new content

### "HTTP 404" errors

**Causes:**
- Feed URL changed or removed
- Website restructured
- Feed discontinued

**Solution:** Remove source or find replacement feed

### "Request timeout"

**Causes:**
- Feed server slow to respond
- Network issues
- High server load

**Solution:** Automatic retry on next scheduled run

### Feed posts old content

**Causes:**
- Date filtering disabled
- Feed has incorrect dates
- Date parsing failed

**Solution:** Check `_is_recent()` method, verify feed dates

---

## Summary

### ✅ What You Don't Need
- API keys
- Registration accounts
- Payment or subscriptions
- Special permissions

### ✅ What You Do Need
- Discord channel IDs (via `.env` or `/news` commands)
- Working internet connection
- Reasonable rate limits (don't spam feeds)

### 📊 Current Stats
- **Total Sources:** 80 working feeds
  - US Legislation: 11 sources (removed 3 broken)
  - EU Legislation: 3 sources
  - News Categories: 73 sources
- **API Keys Required:** 0
- **Cost:** $0 (all free)
- **Setup Time:** < 5 minutes

**You're ready to track news and legislation immediately!** 🚀
