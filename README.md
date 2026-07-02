<p align="center">
<img src="[https://i.postimg.cc/3JjN429B/2ea81f452613dc740e19a5af784425ed.gif](https://i.postimg.cc/3JjN429B/2ea81f452613dc740e19a5af784425ed.gif)" alt="Ollie Bot">
</p>
# OLLIE ⚫
A production-ready Telegram Welcome Bot built with **Aiogram 3.x** and **PostgreSQL**.
### 👨‍💻 Developer
**Yousef Z. A. Shaheen 👑**
<img src="[https://i.postimg.cc/tgrqP2sW/IMG-20260620-133210-543.jpg](https://i.postimg.cc/tgrqP2sW/IMG-20260620-133210-543.jpg)" width="100">
**For contact: 📩**
 * **INSTAGRAM:** @1.0_v_ <img src="https://i.postimg.cc/BbKNsJWZ/9ad79bcb73e8721663f873970d927b40.jpg" width="20">
 * **TELEGRAM:** @Y9_S4 <img src="https://i.postimg.cc/XJXQHwQ9/7cc98f0f748788604c632f6b5736a815.jpg" width="20">
 * **WHATSAPP:** 🔗 Link <img src="[https://i.postimg.cc/Z5F7CYWx/ff71e97414c40fc94af8e192ae16793a.jpg](https://i.postimg.cc/Z5F7CYWx/ff71e97414c40fc94af8e192ae16793a.jpg)" width="20">
 * **TIKTOK:** @zix8ii <img src="https://i.postimg.cc/g0zMR9Rz/b2f532b8bf6aab51b8854971e4ddb210.jpg" width="20">
 * **SNAP CHAT:** @fi1_oo <img src="https://i.postimg.cc/prF917D8/a41e3010fda64b3bcf0589364926e040.jpg" width="20">
 * **FACEBOOK:** Yousef Z. Shaheen <img src="[https://i.postimg.cc/tRZBFN1Z/73b610cbcd0296935a5849dbeccb7bdb.jpg](https://i.postimg.cc/tRZBFN1Z/73b610cbcd0296935a5849dbeccb7bdb.jpg)" width="20">
## Features
 * Sends a customisable welcome message when a new member joins a group
 * Supports unlimited inline URL buttons attached to the welcome message
 * Fully async — built on Aiogram 3.x and asyncpg
 * Multi-group support — each group has its own independent configuration
 * Admin-only management commands
 * HTML parse mode with placeholder support
 * Broadcast system for reaching all known chats
 * Channel tracking (informational)
 * Structured logging
 * Railway-ready deployment
## Commands
| Command | Description |
|---|---|
| /start | Show main menu |
| /set_welcome <text> | Set the welcome message for this group |
| /show_welcome | Preview the current welcome message |
| /del_welcome | Delete the welcome message and all buttons |
| /add_button <label> | <url> | Add an inline button to the welcome message |
| /del_button <id> | Remove a button by its ID |
| /list_buttons | List all configured buttons |
| /add_channel | Register a channel (reply to forwarded msg, or pass @username / ID) |
| /del_channel <channel_id> | Remove a registered channel |
| /list_channels | List all registered channels |
| /broadcast | Send a message to all known chats (super-admin only) |
| /stats | Show bot statistics |
| /cancel | Cancel the current operation |
Management commands are restricted to group administrators and owners.
/broadcast is restricted to user IDs listed in BROADCAST_ADMIN_IDS.
## Placeholders
Use these inside your welcome message text:
| Placeholder | Replaced with |
|---|---|
| {name} | The new member's full name |
| {chat} | The group's name |
Example:
```
/set_welcome Hello, {name}! Welcome to <b>{chat}</b> 🎉

```
## Setup
### Local development
 1. Clone the repository.
 2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
   ```
 3. Copy .env.example to .env and fill in the required values:
   ```bash
   cp .env.example .env
   
   ```
 4. Run the bot:
   ```bash
   python bot.py
   
   ```
### Railway deployment
 1. Create a new Railway project and link this repository.
 2. Add the **PostgreSQL** plugin — Railway injects DATABASE_URL automatically.
 3. Set BOT_TOKEN in the Railway environment variables dashboard.
 4. Set BROADCAST_ADMIN_IDS (optional) to your Telegram user ID(s).
 5. Deploy — Railway uses railway.toml to build and start the bot.
## Environment Variables
| Variable | Required | Default | Description |
|---|---|---|---|
| BOT_TOKEN | ✅ | — | Telegram bot token from @BotFather |
| DATABASE_URL | ✅ | — | PostgreSQL connection string (injected by Railway) |
| BROADCAST_ADMIN_IDS | ❌ | *(empty)* | Comma-separated Telegram user IDs for /broadcast |
| LOG_LEVEL | ❌ | INFO | Logging level: DEBUG, INFO, WARNING, ERROR |
| TZ | ❌ | UTC | Timezone string for log timestamps |
| MAX_CONCURRENT_TASKS | ❌ | 2 | Max concurrent broadcast tasks |
| START_FROM_LATEST | ❌ | true | Drop updates queued while the bot was offline |
See .env.example for a fully commented template.
## Requirements
 * Python 3.12+
 * aiogram 3.20.0
 * asyncpg 0.30.0
 * python-dotenv 1.2.2
## Database
The bot uses **PostgreSQL** exclusively. On first startup it creates four tables:
| Table | Purpose |
|---|---|
| welcome_messages | Stores welcome text per chat |
| buttons | Inline buttons linked to welcome messages |
| channels | Registered channels (informational) |
| known_chats | Broadcast target tracking |
No migrations are required — tables are created with CREATE TABLE IF NOT EXISTS.
## License
MIT
