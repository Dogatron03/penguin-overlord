# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Fortune Cog - Cyber Fortune Cookie with infosec wisdom (sarcastic and real).
"""

import logging
import random
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


# Cyber Fortune Cookie quotes - mix of sarcastic and real infosec wisdom
CYBER_FORTUNES = [
    # Sarcastic wisdom
    {"quote": "Your password is strong. So strong that even you can't remember it.", "sarcastic": True},
    {"quote": "A SQL injection walks into a bar. The bartender says, 'We don't serve your kind here.' The injection replies, 'That's OK, I brought my own table.'", "sarcastic": True},
    {"quote": "Remember: The 'S' in IoT stands for Security.", "sarcastic": True},
    {"quote": "Your two-factor authentication is working perfectly. Both factors are equally vulnerable.", "sarcastic": True},
    {"quote": "Congratulations! You've been using the same password since 2008. Consistency is key.", "sarcastic": True},
    {"quote": "The cloud is just someone else's computer. And they're probably as bad at security as you are.", "sarcastic": True},
    {"quote": "Your API keys are safe in that public GitHub repo. Nobody reads documentation anyway.", "sarcastic": True},
    {"quote": "Don't worry about that certificate error. What's the worst that could happen?", "sarcastic": True},
    {"quote": "Your firewall is working great. It's blocking everything except the hackers.", "sarcastic": True},
    {"quote": "Yes, admin/admin is a perfectly reasonable default credential. It's easy to remember!", "sarcastic": True},
    {"quote": "That suspicious email from 'IT Department' asking for your password? Totally legit.", "sarcastic": True},
    {"quote": "Your company's security is like a screen door on a submarine. But at least you have one!", "sarcastic": True},
    {"quote": "Penetration testing is just hacking with permission and a invoice.", "sarcastic": True},
    {"quote": "Your database backup strategy: Hope nothing bad happens.", "sarcastic": True},
    {"quote": "Security through obscurity works great. Until someone Googles it.", "sarcastic": True},
    
    # Real infosec wisdom
    {"quote": "The only truly secure system is one that is powered off, cast in a block of concrete and sealed in a lead-lined room with armed guards. - Gene Spafford", "sarcastic": False},
    {"quote": "In security, the key is not to have all the answers but to ask the right questions. - Marcus Ranum", "sarcastic": False},
    {"quote": "Passwords are like underwear: you don't let people see it, you should change it regularly, and you shouldn't share it with strangers. - Chris Pirillo", "sarcastic": False},
    {"quote": "If you spend more on coffee than on IT security, you will be hacked. What's more, you deserve to be hacked. - Richard Clarke", "sarcastic": False},
    {"quote": "There are two types of companies: those that have been hacked, and those that don't know they've been hacked.", "sarcastic": False},
    {"quote": "Security is always excessive until it's not enough. - Robbie Sinclair", "sarcastic": False},
    {"quote": "The weakest link in any security chain is the human element.", "sarcastic": False},
    {"quote": "Defense in depth: Because one layer of security is just a speed bump for attackers.", "sarcastic": False},
    {"quote": "Assume breach. It's not paranoia if they're really out to get you.", "sarcastic": False},
    {"quote": "You can't protect what you don't know you have. Asset inventory is security 101.", "sarcastic": False},
    {"quote": "Encryption is the mathematical guarantee of security. Implementation is the engineering guarantee of failure.", "sarcastic": False},
    {"quote": "Zero trust: Verify everything, trust nothing.", "sarcastic": False},
    {"quote": "A backup is only as good as its last successful restore.", "sarcastic": False},
    {"quote": "Incident response: Because 'when' is more realistic than 'if'.", "sarcastic": False},
    {"quote": "Patch management: The only thing worse than applying patches is not applying patches.", "sarcastic": False},
    {"quote": "Your security posture should be good enough to make attackers choose easier targets.", "sarcastic": False},
    {"quote": "Security awareness training: Because humans are both your greatest strength and your biggest vulnerability.", "sarcastic": False},
    {"quote": "Defense requires vigilance. Offense just needs one mistake.", "sarcastic": False},
    {"quote": "Logging: The difference between knowing you were hacked and proving you were hacked.", "sarcastic": False},
    {"quote": "Multi-factor authentication: Because one factor is no longer enough.", "sarcastic": False},
    
    # Additional sarcastic wisdom
    {"quote": "Your antivirus software detected 0 threats. Congratulations on being the first person never to visit a malicious website!", "sarcastic": True},
    {"quote": "Port 22 open to the world? That's just being friendly and accessible!", "sarcastic": True},
    {"quote": "Who needs a WAF when you can just ask hackers nicely not to attack?", "sarcastic": True},
    {"quote": "Your password complexity requirement of 8 characters will surely stop nation-state actors.", "sarcastic": True},
    {"quote": "Clicking 'Remind me later' on security updates is basically the same as installing them.", "sarcastic": True},
    {"quote": "Your network segmentation strategy: Everything can talk to everything. It's more democratic this way.", "sarcastic": True},
    {"quote": "Shadow IT? More like 'innovation without red tape'!", "sarcastic": True},
    {"quote": "Your incident response plan is stored on the server that just got ransomwared. Perfect.", "sarcastic": True},
    {"quote": "Storing passwords in a text file named 'not_passwords.txt' is galaxy-brain security.", "sarcastic": True},
    {"quote": "Your security audit found 50 critical vulnerabilities. But that's next quarter's problem, right?", "sarcastic": True},
    {"quote": "Why patch today when you can patch never?", "sarcastic": True},
    {"quote": "Your password hint is the password. Efficiency at its finest!", "sarcastic": True},
    {"quote": "Disabling SSL verification in production is just removing unnecessary friction.", "sarcastic": True},
    {"quote": "Your security policy is 'YOLO'. Short, memorable, and completely ineffective.", "sarcastic": True},
    {"quote": "Using 'password123' for everything means only one password to remember. Smart!", "sarcastic": True},
    {"quote": "That vulnerability is only theoretical. Until someone exploits it.", "sarcastic": True},
    {"quote": "Your web server is running as root. Because privilege separation is for cowards.", "sarcastic": True},
    {"quote": "Debug mode in production gives attackers that warm, fuzzy feeling.", "sarcastic": True},
    {"quote": "Security through obscurity is fine. Nobody would ever scan your network anyway.", "sarcastic": True},
    {"quote": "Your SIEM is collecting so many logs, none of which anyone will ever read.", "sarcastic": True},
    {"quote": "Commenting out authentication checks is a valid troubleshooting step. Just remember to uncomment them. You won't.", "sarcastic": True},
    {"quote": "Your company's cybersecurity budget: $0. Your ransomware payment budget: $500,000.", "sarcastic": True},
    {"quote": "Clicking 'Accept All Cookies' is the digital equivalent of inviting vampires into your home.", "sarcastic": True},
    {"quote": "Your air-gapped network is connected to WiFi. That's still air, right?", "sarcastic": True},
    {"quote": "Root credentials in environment variables? At least they're not hardcoded. Oh wait, they are.", "sarcastic": True},
    {"quote": "Your security awareness training: A 5-minute video watched at 2x speed.", "sarcastic": True},
    {"quote": "Telnet is vintage. Retro is cool. Your security posture is neither.", "sarcastic": True},
    {"quote": "Why use HTTPS when HTTP is 4 characters shorter and faster to type?", "sarcastic": True},
    {"quote": "Your IDS is so sensitive, it alerts on everything. So you ignore everything. Perfect balance.", "sarcastic": True},
    {"quote": "Email from 'Microsoft Support'? Seems legit. Better send them your credit card info.", "sarcastic": True},
    {"quote": "Your disaster recovery plan: Panic first, think later.", "sarcastic": True},
    {"quote": "chmod 777 solves all permission problems and creates exciting new security problems!", "sarcastic": True},
    {"quote": "Your VPN is always on. Too bad your security awareness isn't.", "sarcastic": True},
    {"quote": "Hardcoded credentials: Because configuration files are too mainstream.", "sarcastic": True},
    {"quote": "Your docker containers run as root. What could possibly go wrong?", "sarcastic": True},
    {"quote": "That USB drive you found in the parking lot? Definitely doesn't contain malware.", "sarcastic": True},
    {"quote": "Security patches can wait. That legacy system only handles critical business functions.", "sarcastic": True},
    {"quote": "Your password policy: Must contain at least one sticky note under the keyboard.", "sarcastic": True},
    {"quote": "Disabling the firewall fixed the connectivity issue. Problem solved forever!", "sarcastic": True},
    {"quote": "Your ransomware backup strategy: The same server that just got encrypted.", "sarcastic": True},
    {"quote": "SQL injection? Just add more quotes. Problem solved!", "sarcastic": True},
    {"quote": "Your security questions: Mother's maiden name? It's on Facebook.", "sarcastic": True},
    {"quote": "That browser extension wants access to all websites? Seems reasonable.", "sarcastic": True},
    {"quote": "Your JWT secret is 'secret'. At least it's honest.", "sarcastic": True},
    {"quote": "Phishing simulation results: 80% click rate. Your users are very helpful!", "sarcastic": True},
    {"quote": "Your database is publicly accessible. That's just good API design, right?", "sarcastic": True},
    {"quote": "Why encrypt backups when you can save time and just lose data faster?", "sarcastic": True},
    {"quote": "Your error messages leak stack traces. Think of it as helpful documentation for attackers.", "sarcastic": True},
    
    # Additional real wisdom
    {"quote": "Security is not a product, but a process. - Bruce Schneier", "sarcastic": False},
    {"quote": "The attacker only needs to find one weakness. The defender needs to find all of them.", "sarcastic": False},
    {"quote": "Perfect security is impossible. Good security is mandatory.", "sarcastic": False},
    {"quote": "An ounce of prevention is worth a pound of incident response.", "sarcastic": False},
    {"quote": "Network segmentation: Contain the breach before it becomes a catastrophe.", "sarcastic": False},
    {"quote": "Your security monitoring is only as good as the alerts you actually investigate.", "sarcastic": False},
    {"quote": "Threat modeling: Think like an attacker before they think about you.", "sarcastic": False},
    {"quote": "Security is a journey, not a destination. And it's uphill both ways.", "sarcastic": False},
    {"quote": "The best time to implement security was at design time. The second best time is now.", "sarcastic": False},
    {"quote": "Compliance is the minimum. Security is the goal.", "sarcastic": False},
    {"quote": "Data classification: You can't protect everything equally, so protect what matters most.", "sarcastic": False},
    {"quote": "Security culture starts at the top and permeates the entire organization.", "sarcastic": False},
    {"quote": "Automation is the key to consistent security at scale.", "sarcastic": False},
    {"quote": "Your security team should be an enabler, not a blocker.", "sarcastic": False},
    {"quote": "Secure development practices: Build security in, don't bolt it on later.", "sarcastic": False},
    {"quote": "Risk management is about making informed decisions, not eliminating all risk.", "sarcastic": False},
    {"quote": "Privileged access management: Minimize privileges, maximize accountability.", "sarcastic": False},
    {"quote": "Security metrics should drive decisions, not just fill dashboards.", "sarcastic": False},
    {"quote": "Continuous monitoring beats periodic assessments every time.", "sarcastic": False},
    {"quote": "An effective security program requires people, processes, and technology in that order.", "sarcastic": False},
    {"quote": "Vulnerability management: Find them, fix them, verify them, repeat.", "sarcastic": False},
    {"quote": "Your security posture is only as strong as your weakest third-party vendor.", "sarcastic": False},
    {"quote": "Identity and access management: The right person, with the right access, at the right time.", "sarcastic": False},
    {"quote": "Security awareness is not a one-time training. It's a continuous campaign.", "sarcastic": False},
    {"quote": "Defense in depth means multiple layers. One layer is not depth.", "sarcastic": False},
    {"quote": "Tabletop exercises: Practice your incident response before you need it.", "sarcastic": False},
    {"quote": "Your security tools are worthless if they're not properly configured and maintained.", "sarcastic": False},
    {"quote": "Threat intelligence: Know your adversaries and their tactics.", "sarcastic": False},
    {"quote": "Security by design means considering security at every phase of development.", "sarcastic": False},
    {"quote": "Data loss prevention: Because not all data should be shareable.", "sarcastic": False},
    {"quote": "Your attack surface area directly correlates with your risk exposure.", "sarcastic": False},
    {"quote": "Strong authentication is the foundation of secure access.", "sarcastic": False},
    {"quote": "Separation of duties prevents single points of failure and fraud.", "sarcastic": False},
    {"quote": "Security orchestration: Coordinate your defenses like a symphony.", "sarcastic": False},
    {"quote": "Purple teaming: When red and blue work together, everyone wins.", "sarcastic": False},
    {"quote": "Your security roadmap should align with business objectives.", "sarcastic": False},
    {"quote": "Cryptographic agility: Be ready to upgrade your encryption before it's broken.", "sarcastic": False},
    {"quote": "Security testing should be integrated into your CI/CD pipeline.", "sarcastic": False},
    {"quote": "Least privilege: Grant only the minimum access required to do the job.", "sarcastic": False},
    {"quote": "Your security documentation should be living documents, not ancient artifacts.", "sarcastic": False},
    {"quote": "Know your assets, know your threats, know your defenses.", "sarcastic": False},
    {"quote": "Security champions within teams spread security knowledge better than central teams alone.", "sarcastic": False},
    {"quote": "Regular security assessments reveal gaps before attackers do.", "sarcastic": False},
    {"quote": "Your network traffic should be monitored, but also understood.", "sarcastic": False},
    {"quote": "Security debt accumulates interest in the form of increased risk.", "sarcastic": False},
    {"quote": "Defense requires understanding both your assets and your adversaries.", "sarcastic": False},
    {"quote": "Configuration management: Consistency is security.", "sarcastic": False},
    {"quote": "Your crown jewels deserve crown jewel protection.", "sarcastic": False},
    {"quote": "Security governance provides structure; security culture provides motivation.", "sarcastic": False},
    {"quote": "The OWASP Top 10 is a starting point, not a finishing line.", "sarcastic": False},
]


class Fortune(commands.Cog):
    """Cyber Fortune Cookie - Infosec wisdom with a twist."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='fortune', description='Get a cyber fortune cookie')
    async def fortune(self, ctx: commands.Context):
        """
        Get a random cyber fortune cookie with infosec wisdom.
        Can be sarcastic or genuinely helpful!
        
        Usage:
            !fortune
            /fortune
        """
        fortune_data = random.choice(CYBER_FORTUNES)
        
        # Create embed with different colors for sarcastic vs real wisdom
        color = 0xFF6B6B if fortune_data['sarcastic'] else 0x4ECDC4
        wisdom_type = "🍪 Sarcastic Wisdom" if fortune_data['sarcastic'] else "🔐 Real Wisdom"
        
        embed = discord.Embed(
            title=wisdom_type,
            description=fortune_data['quote'],
            color=color
        )
        
        embed.set_footer(text="Cyber Fortune Cookie • Use !fortune for more wisdom")
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Load the Fortune cog."""
    await bot.add_cog(Fortune(bot))
    logger.info("Fortune cog loaded")
