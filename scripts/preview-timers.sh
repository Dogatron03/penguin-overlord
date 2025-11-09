#!/bin/bash
# Test script to show what systemd timers would look like
# (without actually deploying them)

echo "📰 Penguin Bot News System - Systemd Timer Preview"
echo "=================================================="
echo
echo "This shows what would be deployed (run deploy-news-timers.sh with sudo to actually deploy)"
echo

PROJECT_ROOT="/home/chiefgyk3d/src/penguin-overlord"

# Function to show timer configuration
show_timer() {
    local category=$1
    local schedule=$2
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📅 Timer: penguin-news-${category}.timer"
    echo "   Schedule: $schedule"
    echo "   Service: penguin-news-${category}.service"
    echo "   Command: python3 scripts/news_runner.py --category ${category}"
    echo
}

echo "🔧 Configured Timers:"
echo
show_timer "cve" "*-*-* 00,06,12,18:00:00 (Every 6 hours at :00)"
show_timer "cybersecurity" "*-*-* 00,03,06,09,12,15,18,21:01:00 (Every 3 hours at :01)"
show_timer "tech" "*-*-* 00,04,08,12,16,20:30:00 (Every 4 hours at :30)"
show_timer "gaming" "*-*-* */2:15:00 (Every 2 hours at :15)"
show_timer "apple_google" "*-*-* 00,03,06,09,12,15,18,21:45:00 (Every 3 hours at :45)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "📊 Resource Limits (per service):"
echo "   Memory: 256MB max"
echo "   CPU: 50% quota"
echo "   Tasks: 50 max"
echo "   Timeout: 120 seconds"
echo
echo "📁 Files that would be created:"
echo "   /etc/systemd/system/penguin-news-cve.service"
echo "   /etc/systemd/system/penguin-news-cve.timer"
echo "   /etc/systemd/system/penguin-news-cybersecurity.service"
echo "   /etc/systemd/system/penguin-news-cybersecurity.timer"
echo "   /etc/systemd/system/penguin-news-tech.service"
echo "   /etc/systemd/system/penguin-news-tech.timer"
echo "   /etc/systemd/system/penguin-news-gaming.service"
echo "   /etc/systemd/system/penguin-news-gaming.timer"
echo "   /etc/systemd/system/penguin-news-apple_google.service"
echo "   /etc/systemd/system/penguin-news-apple_google.timer"
echo
echo "🚀 To deploy for real:"
echo "   sudo ./scripts/deploy-news-timers.sh"
echo
echo "📋 After deployment, manage with:"
echo "   systemctl status penguin-news-*.timer"
echo "   systemctl list-timers penguin-news-*"
echo "   journalctl -u penguin-news-cybersecurity -f"
echo
