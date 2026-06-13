# Telegram Reporter

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Telethon](https://img.shields.io/badge/Telethon-1.34+-green.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**A Powerful Tool for Reporting Violations on Telegram**

[Installation](#-installation) • [Features](#-features) • [Usage](#-usage) • [Support](#-contact--support)

</div>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b61d9ccd-1a2d-4627-ac08-0dedb70afdd1" alt="Telegram Reporter Banner" width="800">
</p>

---

## 📌 Overview

**Telegram Reporter** is a comprehensive Python-based tool designed to help users report violations on Telegram efficiently. Whether it's spam, violence, child abuse, or any other policy violation, this tool streamlines the reporting process with multi-account support, automated sessions, and a beautiful terminal interface.

> ⚠️ **Disclaimer**: This tool is for educational purposes only. Users are responsible for complying with Telegram's Terms of Service. Misuse may result in account restrictions.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📱 **Multi-Account Support** | Manage multiple Telegram accounts simultaneously |
| 🎯 **8 Report Categories** | Spam, Violence, Child Abuse, Pornography, Copyright, Fake Accounts, Illegal Drugs, Personal Details |
| 💬 **Custom Messages** | Pre-written templates or write your own report messages |
| 🔄 **Batch Reporting** | Send multiple reports (1-50) from each account |
| 🎨 **Beautiful UI** | Colorful terminal interface with ASCII art banners |
| 🔐 **2FA Support** | Full support for two-factor authentication |
| 💾 **Session Management** | Automatic session saving - no repeated logins |
| 📊 **Statistics Tracking** | Track total reports sent per account |
| 🌐 **Smart Target Detection** | Automatically detects users, channels, and groups |
| ⏱️ **Rate Limit Handling** | Smart delays and flood wait handling |

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Telegram API credentials ([Get from my.telegram.org](https://my.telegram.org/apps))

### Step 1: Clone the Repository

```bash
git clone https://github.com/esfelorm/Telegram-Reporter.git
cd Telegram-Reporter
```

### Step 2: Install Dependencies

```bash
pip install telethon asyncio
```

### Step 3: Get API Credentials

1. Go to [my.telegram.org](https://my.telegram.org/apps)
2. Log in with your phone number
3. Create an application
4. Copy your **API ID** and **API Hash**

---

## 📖 Usage

### Basic Commands

```bash
python main.py
```

### First Time Setup

When you first run the tool, you'll need to add an account:

1. Select option `2` (Manage Accounts) from the main menu
2. Choose option `1` (Add new account)
3. Enter your API ID, API Hash, and phone number
4. Enter the verification code sent to your Telegram
5. If you have 2FA enabled, enter your password

### Reporting Flow

1. **Select Account** - Choose from your saved accounts
2. **Enter Target** - Username, ID, or channel link (e.g., `@spammer`, `https://t.me/username`)
3. **Choose Reason** - Select from 8 violation categories
4. **Select Message** - Choose a template or write custom message
5. **Set Count** - Number of reports to send (1-20 recommended)
6. **Confirm & Send** - Review details and start reporting

### Target Formats

| Format | Example |
|--------|---------|
| Username | `@username` |
| User ID | `123456789` |
| Channel Link | `https://t.me/channelname` |
| Group Link | `https://t.me/joinchat/abc123` |

### Report Categories

| # | Category | Report Reason |
|---|----------|---------------|
| 1 | Spam | Unsolicited messages, promotional content |
| 2 | Pornography | Adult content, NSFW material |
| 3 | Violence | Threats, graphic violence, terrorism |
| 4 | Child Abuse | Exploitation, inappropriate content involving minors |
| 5 | Copyright | Unauthorized sharing of copyrighted material |
| 6 | Fake Account | Impersonation, fraudulent profiles |
| 7 | Illegal Drugs | Drug sales, controlled substances |
| 8 | Personal Details | Doxxing, private information sharing |

---

## 🎮 Menu Structure

```
Main Menu
├── 1. Start Reporting
│   ├── Select Account
│   ├── Enter Target
│   ├── Choose Reason
│   ├── Select/Custom Message
│   ├── Set Report Count
│   └── Confirm & Execute
├── 2. Manage Accounts
│   ├── Add New Account
│   ├── List All Accounts
│   ├── Remove Account
│   └── Logout Account (Session Only)
└── 3. Exit
```

---

## 📁 File Structure

```
Telegram-Reporter/
├── main.py                 # Main application file
├── banner.py               # ASCII art banners & VIP info
├── accounts.json           # Account data storage
├── sessions/               # Session files directory
│   └── account_*.session   # Individual account sessions
└── requirements.txt        # Python dependencies
```

---

## 🛠️ Commands Reference

### Account Management

| Action | Description |
|--------|-------------|
| Add Account | Register a new Telegram account |
| List Accounts | View all saved accounts with stats |
| Remove Account | Delete account from system (removes session) |
| Logout Account | Delete session only (keep account info) |

### Reporting

| Action | Description |
|--------|-------------|
| Start Reporting | Begin the reporting process |
| Select Target | Enter username, ID, or link |
| Choose Reason | Select violation category |
| Custom Message | Write your own report text |

---

## 💡 Tips & Best Practices

1. **Don't Over-report** - Sending too many reports quickly may trigger rate limits (FloodWait)
2. **Use Realistic Counts** - 1-5 reports per target is usually sufficient
3. **Respect Delays** - The tool adds random delays (1-2 seconds) between reports
4. **Keep Sessions Active** - Don't delete session files unless necessary
5. **Monitor Account Health** - If accounts get rate-limited, wait before using them again

---

## 🔧 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **FloodWaitError** | Wait the specified time before trying again. The tool handles this automatically |
| **Session Expired** | Re-login when prompted. The session file may have been deleted |
| **Invalid API ID/Hash** | Double-check credentials from my.telegram.org |
| **Phone Number Banned** | Telegram may have restricted the number. Contact Telegram support |
| **2FA Password Error** | Ensure you're using the correct 2FA password for the account |

### Error Codes

```
❌ FloodWaitError: Rate limited - Tool automatically waits
❌ SessionPasswordNeededError: 2FA required - Enter password
❌ PhoneCodeInvalidError: Wrong verification code - Try again
❌ PhoneCodeExpiredError: Code expired - Request new code
```

---

## 📊 Statistics

The tool tracks:
- **Total reports sent** per account (lifetime)
- **Active sessions** count
- **Accounts** added to system
- **Report success/failure** per operation

---

## 🔐 Security

- All API credentials are stored locally in `accounts.json`
- Session files are encrypted by Telethon
- No data is sent to external servers
- Your phone number and credentials never leave your machine

---

## ❓ FAQ

**Q: Is this against Telegram's ToS?**  
A: Reporting legitimate violations is allowed. However, mass reporting or false reporting may violate ToS. Use responsibly.

**Q: Can I get banned for using this?**  
A: If used for legitimate reporting, unlikely. If abused (spamming reports, false reports), your accounts may be restricted.

**Q: How many reports can I send?**  
A: The tool allows 1-50 per operation, but we recommend 1-5 for most cases.

**Q: Does this work with 2FA?**  
A: Yes, full 2FA support is included.

**Q: Can I use multiple accounts?**  
A: Yes! The tool supports unlimited accounts with individual sessions.

---

## 🚧 Future Updates (VIP Version)

The VIP version includes advanced features:

- ✅ Email reporting system (abuse@telegram.org, support@telegram.org, etc.)
- ✅ Multi-user reporting (report multiple targets at once)
- ✅ Story reporting
- ✅ Multi-message reporting
- ✅ Monitoring system (auto-ban detection)
- ✅ Proxy support (SOCKS5/HTTP)
- ✅ Target existence checking
- ✅ Attack timer & duration tracking
- ✅ Import/Export accounts (JSON)
- ✅ Email templates & custom bodies

**Contact for VIP access:** [@MrEsfelurm](https://t.me/MrEsfelurm)

---

## 📞 Contact & Support

- **GitHub:** [github.com/esfelorm](https://github.com/esfelorm)
- **Telegram:** [@esfelorm](https://t.me/esfelorm)

For bug reports, feature requests, or support, please open an issue on GitHub or contact via Telegram.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ Star this repository if you find it useful!**

Made with ❤️ by [esfelorm](https://github.com/esfelorm)

</div>
