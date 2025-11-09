#!/bin/bash
# Quick bot restart script

cd "$(dirname "$0")"

echo "🛑 Stopping bot..."
pkill -f "python.*bot.py" 2>/dev/null
sleep 2

# Check if stopped
if pgrep -f "python.*bot.py" > /dev/null; then
    echo "⚠️  Bot still running, force killing..."
    pkill -9 -f "python.*bot.py"
    sleep 1
fi

echo "✅ Bot stopped"
echo ""
echo "🚀 Starting bot..."
cd penguin-overlord
python3 bot.py &
BOT_PID=$!

sleep 3

# Check if started
if ps -p $BOT_PID > /dev/null 2>&1; then
    echo "✅ Bot is running (PID: $BOT_PID)"
    echo ""
    echo "📋 To view logs:"
    echo "   tail -f /tmp/bot.log"
    echo ""
    echo "📋 To stop:"
    echo "   pkill -f 'python.*bot.py'"
else
    echo "❌ Bot failed to start"
    exit 1
fi
