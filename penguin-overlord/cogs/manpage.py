# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Manpage Cog - Random Linux command snippets from man pages.
"""

import logging
import random
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


# Random useful Linux commands with descriptions
LINUX_COMMANDS = [
    # Dangerous/Fun commands
    {"cmd": "dd if=/dev/zero of=/dev/null", "desc": "The world's most efficient space heater. Does absolutely nothing but looks impressive.", "danger": 1},
    {"cmd": ":(){ :|:& };:", "desc": "Fork bomb. Also known as 'the rabbit function'. DO NOT RUN THIS. It will crash your system.", "danger": 5},
    {"cmd": "sudo rm -rf /", "desc": "The nuclear option. Deletes everything. Please don't actually run this.", "danger": 5},
    {"cmd": "sudo rm -rf / --no-preserve-root", "desc": "Even more nuclear. Bypasses the safety. Seriously, don't.", "danger": 5},
    {"cmd": "cat /dev/urandom | hexdump | grep 'ca fe'", "desc": "Looking for coffee in random data. You'll find it eventually... probably.", "danger": 1},
    {"cmd": "alias please='sudo'", "desc": "Politeness matters, even with your terminal.", "danger": 1},
    {"cmd": "sl", "desc": "Like 'ls', but with more trains. Install with apt-get install sl", "danger": 1},
    {"cmd": "telnet towel.blinkenlights.nl", "desc": "Watch Star Wars in ASCII art. Yes, really.", "danger": 1},
    {"cmd": "nc -l 1337", "desc": "Listen on port 1337 like a true 1337 h4x0r.", "danger": 1},
    {"cmd": "curl parrot.live", "desc": "Watch a dancing parrot in your terminal. Essential system administration.", "danger": 1},
    {"cmd": "sudo !!", "desc": "Forgot sudo? This runs your last command with sudo. Time saver!", "danger": 2},
    {"cmd": "mv ~ /dev/null", "desc": "Move your home directory to /dev/null. Digital minimalism taken too far.", "danger": 5},
    {"cmd": "chmod 777 -R /", "desc": "Give everyone permissions to everything. Security? Never heard of her.", "danger": 5},
    {"cmd": "mkfs.ext4 /dev/sda", "desc": "Format your main drive. Hope you backed up... you didn't, did you?", "danger": 5},
    {"cmd": "yes", "desc": "Prints 'y' forever. Surprisingly useful for auto-accepting prompts. Or spamming.", "danger": 1},
    
    # File operations
    {"cmd": "grep -r 'pattern' /path", "desc": "Search for text recursively. Your best friend for finding that one config line.", "danger": 1},
    {"cmd": "find . -name '*.log' -mtime +30 -delete", "desc": "Delete log files older than 30 days. Spring cleaning for your disk.", "danger": 3},
    {"cmd": "find / -name filename 2>/dev/null", "desc": "Find a file anywhere, silencing permission errors. Hide and seek champion.", "danger": 1},
    {"cmd": "find . -type f -size +100M", "desc": "Find files larger than 100MB. Hunt down the space hogs.", "danger": 1},
    {"cmd": "find . -name '*.txt' -exec grep -l 'pattern' {} \\;", "desc": "Find files containing text. grep and find, the dynamic duo.", "danger": 1},
    {"cmd": "rsync -avz source/ dest/", "desc": "Copy files with progress, resume support, and style. Better than cp.", "danger": 1},
    {"cmd": "rsync -avz --delete source/ dest/", "desc": "Sync directories, deleting files in dest that aren't in source. Use carefully!", "danger": 3},
    {"cmd": "tar -czf archive.tar.gz /path", "desc": "Create a gzipped tarball. Compress all the things!", "danger": 1},
    {"cmd": "tar -xzf archive.tar.gz", "desc": "Extract a gzipped tarball. Memorize this, you'll use it forever.", "danger": 1},
    {"cmd": "tar -xjf archive.tar.bz2", "desc": "Extract bzip2 tarball. j for bzip2, z for gzip, remember it!", "danger": 1},
    {"cmd": "zip -r archive.zip folder/", "desc": "Create a zip archive. For when you need Windows compatibility.", "danger": 1},
    {"cmd": "unzip archive.zip", "desc": "Extract a zip file. Simple and effective.", "danger": 1},
    {"cmd": "gzip file.txt", "desc": "Compress a file with gzip. Creates file.txt.gz and removes original.", "danger": 1},
    {"cmd": "gunzip file.txt.gz", "desc": "Decompress a gzip file. The yin to gzip's yang.", "danger": 1},
    {"cmd": "chmod +x script.sh", "desc": "Make a script executable. One of the first things you Google as a Linux newbie.", "danger": 1},
    {"cmd": "chmod 755 file", "desc": "rwxr-xr-x permissions. The most common chmod you'll use.", "danger": 1},
    {"cmd": "chmod 644 file", "desc": "rw-r--r-- permissions. Standard for regular files.", "danger": 1},
    {"cmd": "chown user:group file", "desc": "Change file ownership. Fix those permission problems!", "danger": 2},
    {"cmd": "chown -R user:group /path", "desc": "Recursively change ownership. Fix ALL the permission problems!", "danger": 2},
    {"cmd": "cp -r source/ dest/", "desc": "Copy directories recursively. Remember the -r!", "danger": 1},
    {"cmd": "cp -p file dest", "desc": "Copy preserving attributes. Timestamps and permissions intact.", "danger": 1},
    {"cmd": "mv oldname newname", "desc": "Move or rename files. Simple but essential.", "danger": 1},
    {"cmd": "rm -rf directory/", "desc": "Recursively delete a directory. Use with caution!", "danger": 3},
    {"cmd": "ln -s /path/to/file symlink", "desc": "Create a symbolic link. Shortcuts for your filesystem.", "danger": 1},
    {"cmd": "touch file.txt", "desc": "Create an empty file or update timestamp. Simple but handy.", "danger": 1},
    {"cmd": "file filename", "desc": "Identify file type. Is it a script? Binary? Compressed? Find out!", "danger": 1},
    {"cmd": "stat filename", "desc": "Detailed file information. Size, permissions, timestamps, inodes.", "danger": 1},
    
    # Text processing
    {"cmd": "cat file.txt", "desc": "Display file contents. The most basic, yet essential command.", "danger": 1},
    {"cmd": "cat file1 file2 > merged.txt", "desc": "Concatenate files. Cat does more than just display!", "danger": 1},
    {"cmd": "tac file.txt", "desc": "Like cat, but backwards. Display file in reverse order.", "danger": 1},
    {"cmd": "less file.txt", "desc": "View file with scrolling. More powerful than more.", "danger": 1},
    {"cmd": "head -n 20 file.txt", "desc": "Show first 20 lines. Quick peek at the beginning.", "danger": 1},
    {"cmd": "tail -n 20 file.txt", "desc": "Show last 20 lines. Great for recent log entries.", "danger": 1},
    {"cmd": "tail -f /var/log/syslog", "desc": "Watch logs in real-time. Perfect for debugging or pretending to work.", "danger": 1},
    {"cmd": "tail -f /var/log/apache2/access.log", "desc": "Watch web server logs live. See visitors in real-time.", "danger": 1},
    {"cmd": "grep 'pattern' file.txt", "desc": "Search for text in files. The sysadmin's best friend.", "danger": 1},
    {"cmd": "grep -i 'pattern' file.txt", "desc": "Case-insensitive search. Because case matters... sometimes.", "danger": 1},
    {"cmd": "grep -v 'pattern' file.txt", "desc": "Inverse match. Show lines that DON'T match.", "danger": 1},
    {"cmd": "grep -n 'pattern' file.txt", "desc": "Show line numbers with matches. Handy for editing.", "danger": 1},
    {"cmd": "grep -A 5 'pattern' file.txt", "desc": "Show 5 lines after match. Context is everything.", "danger": 1},
    {"cmd": "grep -B 5 'pattern' file.txt", "desc": "Show 5 lines before match. More context!", "danger": 1},
    {"cmd": "grep -C 5 'pattern' file.txt", "desc": "Show 5 lines before AND after. All the context!", "danger": 1},
    {"cmd": "egrep 'regex' file.txt", "desc": "Extended regex grep. For when simple patterns aren't enough.", "danger": 1},
    {"cmd": "awk '{print $1}' file.txt", "desc": "Extract the first column. AWK is a Swiss Army chainsaw.", "danger": 1},
    {"cmd": "awk '{sum+=$1} END {print sum}' file.txt", "desc": "Sum a column of numbers. AWK doing AWK things.", "danger": 1},
    {"cmd": "awk -F: '{print $1}' /etc/passwd", "desc": "Custom delimiter. Extract usernames from passwd file.", "danger": 1},
    {"cmd": "sed 's/old/new/g' file.txt", "desc": "Find and replace text. sed is the editor you never knew you needed.", "danger": 1},
    {"cmd": "sed -i 's/old/new/g' file.txt", "desc": "In-place editing. Modify files directly without temp files.", "danger": 2},
    {"cmd": "sed -n '10,20p' file.txt", "desc": "Print lines 10-20. sed for precise line extraction.", "danger": 1},
    {"cmd": "cut -d: -f1 /etc/passwd", "desc": "Extract fields by delimiter. List all usernames.", "danger": 1},
    {"cmd": "sort file.txt", "desc": "Sort lines alphabetically. Simple but powerful.", "danger": 1},
    {"cmd": "sort -n file.txt", "desc": "Numeric sort. Because 10 should come after 9.", "danger": 1},
    {"cmd": "sort -r file.txt", "desc": "Reverse sort. Z to A instead of A to Z.", "danger": 1},
    {"cmd": "sort -u file.txt", "desc": "Sort and remove duplicates. Two commands in one!", "danger": 1},
    {"cmd": "uniq file.txt", "desc": "Remove duplicate adjacent lines. Usually paired with sort.", "danger": 1},
    {"cmd": "uniq -c file.txt", "desc": "Count occurrences of duplicates. Find the most common lines.", "danger": 1},
    {"cmd": "wc -l file.txt", "desc": "Count lines in a file. Simple but frequently needed.", "danger": 1},
    {"cmd": "wc -w file.txt", "desc": "Count words. For when you care about word count.", "danger": 1},
    {"cmd": "wc -c file.txt", "desc": "Count bytes. File size the hard way.", "danger": 1},
    {"cmd": "tr 'a-z' 'A-Z' < file.txt", "desc": "Convert lowercase to uppercase. Character translation.", "danger": 1},
    {"cmd": "tr -d '\\n' < file.txt", "desc": "Delete newlines. Combine all lines into one.", "danger": 1},
    {"cmd": "diff file1 file2", "desc": "Compare two files. See what changed.", "danger": 1},
    {"cmd": "diff -u file1 file2", "desc": "Unified diff format. Human-readable file comparison.", "danger": 1},
    {"cmd": "comm file1 file2", "desc": "Compare sorted files. Shows unique and common lines.", "danger": 1},
    {"cmd": "paste file1 file2", "desc": "Merge lines side by side. Column by column combination.", "danger": 1},
    {"cmd": "join file1 file2", "desc": "Join files by common field. SQL-style join in the shell.", "danger": 1},
    {"cmd": "column -t file.txt", "desc": "Format text into columns. Make tables pretty.", "danger": 1},
    {"cmd": "fold -w 80 file.txt", "desc": "Wrap lines at 80 characters. Old-school line width.", "danger": 1},
    {"cmd": "rev file.txt", "desc": "Reverse each line. Character-by-character backwards.", "danger": 1},
    
    # Process management
    {"cmd": "ps aux", "desc": "List all running processes. Snapshot of system activity.", "danger": 1},
    {"cmd": "ps aux | grep process", "desc": "Find a running process. The aux flags are muscle memory for sysadmins.", "danger": 1},
    {"cmd": "ps -ef", "desc": "Another process list format. BSD vs System V style.", "danger": 1},
    {"cmd": "pgrep processname", "desc": "Find process ID by name. Cleaner than ps | grep.", "danger": 1},
    {"cmd": "pkill processname", "desc": "Kill process by name. No need to find PID first.", "danger": 2},
    {"cmd": "killall processname", "desc": "Kill all processes with this name. Mass termination.", "danger": 3},
    {"cmd": "kill -9 PID", "desc": "Force kill a process. The nuclear option for stuck processes.", "danger": 2},
    {"cmd": "kill -15 PID", "desc": "Graceful shutdown signal. Give the process time to clean up.", "danger": 2},
    {"cmd": "kill -HUP PID", "desc": "Send hangup signal. Often reloads config without restart.", "danger": 2},
    {"cmd": "top", "desc": "Interactive process viewer. Watch system resources in real-time.", "danger": 1},
    {"cmd": "htop", "desc": "Like top, but prettier. Install it. Love it. Never go back.", "danger": 1},
    {"cmd": "atop", "desc": "Advanced system monitor. Even more detailed than htop.", "danger": 1},
    {"cmd": "nice -n 10 command", "desc": "Run command with lower priority. Be nice to other processes.", "danger": 1},
    {"cmd": "renice -n 10 -p PID", "desc": "Change priority of running process. Adjust on the fly.", "danger": 2},
    {"cmd": "nohup command &", "desc": "Run command immune to hangups. Keeps running after logout.", "danger": 1},
    {"cmd": "command &", "desc": "Run command in background. Get your terminal back!", "danger": 1},
    {"cmd": "fg", "desc": "Bring background job to foreground. Take back control.", "danger": 1},
    {"cmd": "bg", "desc": "Resume suspended job in background. Keep it running!", "danger": 1},
    {"cmd": "jobs", "desc": "List background jobs. See what's running in this shell.", "danger": 1},
    {"cmd": "disown", "desc": "Detach job from shell. Survives terminal closure.", "danger": 1},
    {"cmd": "screen", "desc": "Detachable terminal sessions. Your work survives even if SSH doesn't.", "danger": 1},
    {"cmd": "tmux", "desc": "Like screen, but newer and with more features. Start the holy war in the comments.", "danger": 1},
    {"cmd": "tmux attach", "desc": "Reattach to existing tmux session. Continue where you left off.", "danger": 1},
    {"cmd": "watch -n 1 command", "desc": "Run command every second. Monitor changes in real-time.", "danger": 1},
    {"cmd": "time command", "desc": "Measure command execution time. How long did that take?", "danger": 1},
    {"cmd": "timeout 30s command", "desc": "Kill command after 30 seconds. For when things hang.", "danger": 1},
    {"cmd": "at 3pm", "desc": "Schedule command for specific time. One-time cron.", "danger": 1},
    {"cmd": "batch", "desc": "Run command when system load is low. Polite background processing.", "danger": 1},
    
    # System information
    {"cmd": "uname -a", "desc": "System information. Kernel version, hostname, architecture.", "danger": 1},
    {"cmd": "hostname", "desc": "Display system hostname. Simple but essential.", "danger": 1},
    {"cmd": "uptime", "desc": "How long has the system been running? Uptime bragging rights.", "danger": 1},
    {"cmd": "w", "desc": "Who is logged in and what they're doing. Spy on your users!", "danger": 1},
    {"cmd": "who", "desc": "List logged in users. Simpler than w.", "danger": 1},
    {"cmd": "whoami", "desc": "Current username. For when you forget who you are.", "danger": 1},
    {"cmd": "id", "desc": "Show user and group IDs. Am I root yet?", "danger": 1},
    {"cmd": "last", "desc": "Show last logins. User access history.", "danger": 1},
    {"cmd": "lastlog", "desc": "Show last login for each user. Security auditing.", "danger": 1},
    {"cmd": "df -h", "desc": "Check disk space in human-readable format. Always run this before 'disk full' errors.", "danger": 1},
    {"cmd": "df -i", "desc": "Check inode usage. Sometimes you run out of inodes before disk space.", "danger": 1},
    {"cmd": "du -sh *", "desc": "See which directories are eating your disk space. Prepare to be surprised.", "danger": 1},
    {"cmd": "du -sh * | sort -h", "desc": "Disk usage sorted. Find the biggest space hogs.", "danger": 1},
    {"cmd": "ncdu", "desc": "Interactive disk usage. Navigate your filesystem by size.", "danger": 1},
    {"cmd": "free -h", "desc": "Check memory usage. Yes, Linux is using all your RAM as cache. It's fine.", "danger": 1},
    {"cmd": "vmstat 1", "desc": "Virtual memory statistics. Watch system performance.", "danger": 1},
    {"cmd": "iostat", "desc": "I/O statistics. Is your disk the bottleneck?", "danger": 1},
    {"cmd": "iotop", "desc": "Like top, but for disk I/O. Find the I/O hogs.", "danger": 1},
    {"cmd": "lsblk", "desc": "List block devices. See all your disks and partitions.", "danger": 1},
    {"cmd": "blkid", "desc": "Block device attributes. UUIDs and filesystem types.", "danger": 1},
    {"cmd": "fdisk -l", "desc": "List disk partitions. Old school partition viewer.", "danger": 1},
    {"cmd": "parted -l", "desc": "List partitions with parted. More modern than fdisk.", "danger": 1},
    {"cmd": "lscpu", "desc": "CPU information. Cores, threads, architecture.", "danger": 1},
    {"cmd": "lspci", "desc": "List PCI devices. See your hardware.", "danger": 1},
    {"cmd": "lsusb", "desc": "List USB devices. What's plugged in?", "danger": 1},
    {"cmd": "dmidecode", "desc": "Hardware information from BIOS. Deep system details.", "danger": 1},
    {"cmd": "sensors", "desc": "Hardware sensor readings. Temperature, voltage, fan speeds.", "danger": 1},
    {"cmd": "dmesg", "desc": "Kernel ring buffer messages. Boot and hardware logs.", "danger": 1},
    {"cmd": "dmesg | grep -i error", "desc": "Find kernel errors. Troubleshooting 101.", "danger": 1},
    
    # Networking
    {"cmd": "ip addr show", "desc": "Show network interfaces. Modern replacement for ifconfig.", "danger": 1},
    {"cmd": "ip route show", "desc": "Display routing table. Where does traffic go?", "danger": 1},
    {"cmd": "ip link set eth0 up", "desc": "Bring network interface up. Turn it on!", "danger": 2},
    {"cmd": "ifconfig", "desc": "Network interface config. Old school, but still works.", "danger": 1},
    {"cmd": "netstat -tulpn", "desc": "See what's listening on your ports. Great for finding rogue services.", "danger": 1},
    {"cmd": "ss -tulpn", "desc": "Socket statistics. Modern replacement for netstat.", "danger": 1},
    {"cmd": "ss -s", "desc": "Socket statistics summary. Quick overview.", "danger": 1},
    {"cmd": "lsof -i", "desc": "List open network files. What's talking to the network?", "danger": 1},
    {"cmd": "lsof -i :80", "desc": "See what's using port 80. Process detective work.", "danger": 1},
    {"cmd": "nmap localhost", "desc": "Port scan yourself. See what's exposed.", "danger": 1},
    {"cmd": "nmap -sV target", "desc": "Service version detection. Know what's running where.", "danger": 1},
    {"cmd": "ping google.com", "desc": "Test network connectivity. Is it working?", "danger": 1},
    {"cmd": "ping -c 4 google.com", "desc": "Ping 4 times and stop. Civilized pinging.", "danger": 1},
    {"cmd": "traceroute google.com", "desc": "Trace network path. Where does traffic go?", "danger": 1},
    {"cmd": "tracepath google.com", "desc": "Like traceroute, no root needed. Path MTU discovery.", "danger": 1},
    {"cmd": "mtr google.com", "desc": "Continuous traceroute. Ping and trace combined.", "danger": 1},
    {"cmd": "dig google.com", "desc": "DNS lookup. Query domain information.", "danger": 1},
    {"cmd": "dig +short google.com", "desc": "Quick DNS lookup. Just the IP, please.", "danger": 1},
    {"cmd": "nslookup google.com", "desc": "DNS lookup, old school style. Still works!", "danger": 1},
    {"cmd": "host google.com", "desc": "Simple DNS lookup. Quick and dirty.", "danger": 1},
    {"cmd": "whois google.com", "desc": "Domain registration info. Who owns this?", "danger": 1},
    {"cmd": "curl -I https://google.com", "desc": "Get HTTP headers. See server response without body.", "danger": 1},
    {"cmd": "wget https://example.com/file", "desc": "Download files. Simple but reliable.", "danger": 1},
    {"cmd": "wget -r -np https://site.com", "desc": "Mirror a website. Download everything!", "danger": 1},
    {"cmd": "curl https://ifconfig.me", "desc": "Get your public IP. Who am I to the internet?", "danger": 1},
    {"cmd": "nc -zv host 1-1000", "desc": "Port scan with netcat. Manual nmap.", "danger": 1},
    {"cmd": "arp -a", "desc": "View ARP cache. See MAC addresses on your network.", "danger": 1},
    {"cmd": "route -n", "desc": "Display routing table numerically. No DNS lookups.", "danger": 1},
    {"cmd": "iptables -L", "desc": "List firewall rules. See what's blocked.", "danger": 1},
    {"cmd": "tcpdump -i eth0", "desc": "Capture network packets. Network debugging.", "danger": 1},
    {"cmd": "tcpdump -i any port 80", "desc": "Capture HTTP traffic. See web requests.", "danger": 1},
    {"cmd": "ethtool eth0", "desc": "Network interface driver info. Speed, duplex, link status.", "danger": 1},
    
    # SSH and remote
    {"cmd": "ssh user@host", "desc": "Connect to remote system. Remote shell access.", "danger": 1},
    {"cmd": "ssh -p 2222 user@host", "desc": "SSH on custom port. Not everyone uses 22.", "danger": 1},
    {"cmd": "ssh -L 8080:localhost:80 user@host", "desc": "SSH tunnel magic. Access remote services like they're local.", "danger": 1},
    {"cmd": "ssh -R 8080:localhost:80 user@host", "desc": "Reverse SSH tunnel. Expose local service to remote.", "danger": 2},
    {"cmd": "ssh -D 1080 user@host", "desc": "Dynamic port forwarding. SOCKS proxy through SSH.", "danger": 1},
    {"cmd": "ssh -X user@host", "desc": "SSH with X11 forwarding. Run GUI apps remotely.", "danger": 1},
    {"cmd": "scp file user@host:/path", "desc": "Copy file over SSH. Secure file transfer.", "danger": 1},
    {"cmd": "scp -r dir/ user@host:/path", "desc": "Recursively copy directory over SSH.", "danger": 1},
    {"cmd": "ssh-keygen -t rsa -b 4096", "desc": "Generate SSH key pair. Password-less authentication.", "danger": 1},
    {"cmd": "ssh-copy-id user@host", "desc": "Copy SSH key to remote. Setup password-less login.", "danger": 1},
    {"cmd": "ssh-add ~/.ssh/id_rsa", "desc": "Add key to SSH agent. Use keys without password prompts.", "danger": 1},
    
    # Package management (Debian/Ubuntu)
    {"cmd": "apt update", "desc": "Update package lists. Know what's available.", "danger": 1},
    {"cmd": "apt upgrade", "desc": "Upgrade installed packages. Keep system updated.", "danger": 2},
    {"cmd": "apt full-upgrade", "desc": "Upgrade with dependency changes. Major updates.", "danger": 2},
    {"cmd": "apt install package", "desc": "Install a package. Get new software.", "danger": 1},
    {"cmd": "apt remove package", "desc": "Remove a package. Clean up unwanted software.", "danger": 2},
    {"cmd": "apt purge package", "desc": "Remove package and configs. Complete removal.", "danger": 2},
    {"cmd": "apt autoremove", "desc": "Remove orphaned packages. Clean up dependencies.", "danger": 2},
    {"cmd": "apt search keyword", "desc": "Search for packages. Find what you need.", "danger": 1},
    {"cmd": "apt show package", "desc": "Show package details. What does this do?", "danger": 1},
    {"cmd": "apt list --installed", "desc": "List installed packages. What's on my system?", "danger": 1},
    {"cmd": "dpkg -l", "desc": "List installed packages. Lower level than apt.", "danger": 1},
    {"cmd": "dpkg -i package.deb", "desc": "Install local .deb file. Manual package install.", "danger": 2},
    {"cmd": "dpkg -r package", "desc": "Remove package with dpkg. Low level removal.", "danger": 2},
    {"cmd": "dpkg -L package", "desc": "List files installed by package. Where did it put things?", "danger": 1},
    {"cmd": "dpkg -S /path/to/file", "desc": "Find which package owns a file. Package archaeology.", "danger": 1},
    
    # Package management (RHEL/CentOS/Fedora)
    {"cmd": "yum update", "desc": "Update packages (RHEL/CentOS). Keep system current.", "danger": 2},
    {"cmd": "yum install package", "desc": "Install package with yum. Get new software.", "danger": 1},
    {"cmd": "yum remove package", "desc": "Remove package with yum. Clean up.", "danger": 2},
    {"cmd": "yum search keyword", "desc": "Search for packages. Find what you need.", "danger": 1},
    {"cmd": "dnf update", "desc": "Update packages (Fedora). Modern yum replacement.", "danger": 2},
    {"cmd": "dnf install package", "desc": "Install with dnf. Fedora's package manager.", "danger": 1},
    {"cmd": "rpm -qa", "desc": "List all installed RPM packages. What's installed?", "danger": 1},
    {"cmd": "rpm -qi package", "desc": "Query RPM package info. Package details.", "danger": 1},
    {"cmd": "rpm -ql package", "desc": "List files in RPM package. Where are the files?", "danger": 1},
    {"cmd": "rpm -qf /path/to/file", "desc": "Find which RPM owns file. Package detective.", "danger": 1},
    
    # Systemd/Services
    {"cmd": "systemctl status service", "desc": "Check service status. Is it running?", "danger": 1},
    {"cmd": "systemctl start service", "desc": "Start a service. Turn it on!", "danger": 2},
    {"cmd": "systemctl stop service", "desc": "Stop a service. Turn it off!", "danger": 2},
    {"cmd": "systemctl restart service", "desc": "Restart a service. Common after config changes.", "danger": 2},
    {"cmd": "systemctl reload service", "desc": "Reload service config. No downtime restart.", "danger": 2},
    {"cmd": "systemctl enable service", "desc": "Enable service at boot. Start automatically.", "danger": 2},
    {"cmd": "systemctl disable service", "desc": "Disable service at boot. Don't start automatically.", "danger": 2},
    {"cmd": "systemctl list-units", "desc": "List all units. See everything systemd manages.", "danger": 1},
    {"cmd": "systemctl list-units --failed", "desc": "List failed units. What's broken?", "danger": 1},
    {"cmd": "journalctl", "desc": "View systemd logs. Modern log viewing.", "danger": 1},
    {"cmd": "journalctl -xe", "desc": "Read systemd logs. Because systemd owns your boot process now.", "danger": 1},
    {"cmd": "journalctl -u service", "desc": "View logs for specific service. Targeted debugging.", "danger": 1},
    {"cmd": "journalctl -f", "desc": "Follow journal in real-time. Like tail -f for systemd.", "danger": 1},
    {"cmd": "journalctl --since today", "desc": "Today's logs only. Filter by time.", "danger": 1},
    {"cmd": "journalctl --since '1 hour ago'", "desc": "Recent logs. Last hour's activity.", "danger": 1},
    
    # Compression
    {"cmd": "gzip -9 file", "desc": "Maximum compression with gzip. Squeeze it hard!", "danger": 1},
    {"cmd": "bzip2 file", "desc": "Compress with bzip2. Better compression, slower.", "danger": 1},
    {"cmd": "xz file", "desc": "Compress with xz. Best compression ratio.", "danger": 1},
    {"cmd": "7z a archive.7z files", "desc": "Create 7z archive. Excellent compression.", "danger": 1},
    {"cmd": "zcat file.gz", "desc": "View compressed file without extracting. Peek inside!", "danger": 1},
    {"cmd": "zgrep pattern file.gz", "desc": "Grep compressed files. No extraction needed.", "danger": 1},
    
    # Disk operations
    {"cmd": "dd if=/dev/sda of=/dev/sdb bs=4M", "desc": "Clone entire disk. Bit-by-bit copy.", "danger": 4},
    {"cmd": "dd if=/dev/zero of=file bs=1M count=100", "desc": "Create 100MB file of zeros. Test file creation.", "danger": 1},
    {"cmd": "mount /dev/sdb1 /mnt", "desc": "Mount filesystem. Make disk accessible.", "danger": 2},
    {"cmd": "umount /mnt", "desc": "Unmount filesystem. Safely disconnect disk.", "danger": 2},
    {"cmd": "mount -o remount,ro /", "desc": "Remount root as read-only. Emergency mode.", "danger": 3},
    {"cmd": "fsck /dev/sdb1", "desc": "Check filesystem for errors. Run when unmounted!", "danger": 3},
    {"cmd": "e2fsck -f /dev/sdb1", "desc": "Force ext filesystem check. Thorough scan.", "danger": 3},
    {"cmd": "mkfs.ext4 /dev/sdb1", "desc": "Format partition as ext4. Creates filesystem.", "danger": 4},
    {"cmd": "resize2fs /dev/sdb1", "desc": "Resize ext filesystem. Grow or shrink.", "danger": 3},
    {"cmd": "tune2fs -l /dev/sdb1", "desc": "View ext filesystem parameters. Detailed info.", "danger": 1},
    
    # Miscellaneous useful
    {"cmd": "history", "desc": "Show command history. What did I type?", "danger": 1},
    {"cmd": "history | grep command", "desc": "Search command history. Find that command you used last week.", "danger": 1},
    {"cmd": "!!", "desc": "Repeat last command. Quick redo.", "danger": 1},
    {"cmd": "!$", "desc": "Last argument of previous command. Reuse arguments.", "danger": 1},
    {"cmd": "cd -", "desc": "Change to previous directory. Quick directory toggle.", "danger": 1},
    {"cmd": "pushd /path", "desc": "Push directory onto stack. Save location for later.", "danger": 1},
    {"cmd": "popd", "desc": "Pop directory from stack. Return to saved location.", "danger": 1},
    {"cmd": "dirs", "desc": "Show directory stack. Where have I been?", "danger": 1},
    {"cmd": "printenv", "desc": "Show all environment variables. What's set?", "danger": 1},
    {"cmd": "export VAR=value", "desc": "Set environment variable. Configure your session.", "danger": 1},
    {"cmd": "echo $PATH", "desc": "Show PATH variable. Where does shell look for commands?", "danger": 1},
    {"cmd": "which command", "desc": "Show path to command. Where is this program?", "danger": 1},
    {"cmd": "whereis command", "desc": "Locate binary, source, and man page. Find everything.", "danger": 1},
    {"cmd": "type command", "desc": "Display command type. Is it builtin, alias, or file?", "danger": 1},
    {"cmd": "alias ll='ls -lah'", "desc": "Create command alias. Customize your shell.", "danger": 1},
    {"cmd": "unalias ll", "desc": "Remove alias. Undo customization.", "danger": 1},
    {"cmd": "xargs", "desc": "Build command lines from input. Powerful command combiner.", "danger": 1},
    {"cmd": "find . -name '*.txt' | xargs grep pattern", "desc": "Find files and search them. Combine find and grep.", "danger": 1},
    {"cmd": "parallel", "desc": "Run commands in parallel. GNU parallel for speed.", "danger": 1},
    {"cmd": "tee file.txt", "desc": "Read from stdin and write to stdout AND file. Split output.", "danger": 1},
    {"cmd": "command | tee -a file.txt", "desc": "Append to file while showing output. View and save.", "danger": 1},
    {"cmd": "script session.log", "desc": "Record terminal session. Capture everything.", "danger": 1},
    {"cmd": "strace -p PID", "desc": "See what a process is doing at the syscall level. For when debugging gets serious.", "danger": 1},
    {"cmd": "ltrace command", "desc": "Trace library calls. Debug library interactions.", "danger": 1},
    {"cmd": "ldd /bin/ls", "desc": "Show shared library dependencies. What does this need?", "danger": 1},
    {"cmd": "md5sum file", "desc": "Calculate MD5 checksum. Verify file integrity.", "danger": 1},
    {"cmd": "sha256sum file", "desc": "Calculate SHA256 checksum. Better than MD5.", "danger": 1},
    {"cmd": "diff -r dir1/ dir2/", "desc": "Recursively compare directories. Find all differences.", "danger": 1},
    {"cmd": "rsync -avz --dry-run src/ dst/", "desc": "Dry run sync. See what would change without changing.", "danger": 1},
    {"cmd": "date", "desc": "Show current date and time. What time is it?", "danger": 1},
    {"cmd": "date +%Y-%m-%d", "desc": "Custom date format. ISO 8601 date.", "danger": 1},
    {"cmd": "cal", "desc": "Display calendar. What day is it?", "danger": 1},
    {"cmd": "bc", "desc": "Calculator. Do math in the terminal.", "danger": 1},
    {"cmd": "echo 'scale=2; 22/7' | bc", "desc": "Calculate with precision. Pi approximation.", "danger": 1},
    {"cmd": "factor 1234567", "desc": "Prime factorization. Math nerd's delight.", "danger": 1},
    {"cmd": "seq 1 10", "desc": "Generate sequence of numbers. Useful in scripts.", "danger": 1},
    {"cmd": "shuf file.txt", "desc": "Randomly shuffle lines. Randomize order.", "danger": 1},
    {"cmd": "shuf -n 1 file.txt", "desc": "Pick random line from file. Random selection.", "danger": 1},
    {"cmd": "base64 file", "desc": "Encode file to base64. Text-safe binary.", "danger": 1},
    {"cmd": "base64 -d file", "desc": "Decode base64. Reverse encoding.", "danger": 1},
    {"cmd": "hexdump -C file", "desc": "Hex dump of file. See raw bytes.", "danger": 1},
    {"cmd": "strings binary", "desc": "Extract strings from binary. Find readable text.", "danger": 1},
    {"cmd": "xxd file", "desc": "Hex dump with reverse capability. Hex editor lite.", "danger": 1},
    {"cmd": "od -c file", "desc": "Octal dump as characters. Alternative hex dump.", "danger": 1},
]


class Manpage(commands.Cog):
    """Random Linux Command Bot - Man page snippets."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='manpage', description='Get a random Linux command')
    async def manpage(self, ctx: commands.Context):
        """
        Get a random Linux command with description.
        May include both useful and dangerous commands - use with caution!
        
        Usage:
            !manpage
            /manpage
        """
        cmd_data = random.choice(LINUX_COMMANDS)
        
        # Color based on danger level
        if cmd_data['danger'] >= 4:
            color = 0xFF0000  # Red for dangerous
            danger_emoji = "☠️"
        elif cmd_data['danger'] >= 3:
            color = 0xFF6B00  # Orange for caution
            danger_emoji = "⚠️"
        else:
            color = 0x00D166  # Green for safe
            danger_emoji = "✅"
        
        embed = discord.Embed(
            title=f"{danger_emoji} Random Linux Command",
            color=color
        )
        
        embed.add_field(name="Command", value=f"`{cmd_data['cmd']}`", inline=False)
        embed.add_field(name="Description", value=cmd_data['desc'], inline=False)
        
        if cmd_data['danger'] >= 4:
            embed.add_field(
                name="⚠️ WARNING ⚠️", 
                value="This command is dangerous! Do NOT run it unless you know exactly what you're doing!", 
                inline=False
            )
        
        embed.set_footer(text="man page • Use !manpage for more commands")
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Load the Manpage cog."""
    await bot.add_cog(Manpage(bot))
    logger.info("Manpage cog loaded")
