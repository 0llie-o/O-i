<p align="center">
  <img src="https://i.postimg.cc/3JjN429B/2ea81f452613dc740e19a5af784425ed.gif" width="100%" alt="Ollie Banner">
</p>

<h1 align="center">⚫ Ollie</h1>

<p align="center">
A production-ready Telegram Welcome Bot built with <b>Aiogram 3.x</b> and <b>PostgreSQL</b>.
</p>

---

# ✨ Features

- Sends a customizable welcome message when a new member joins a group
- Supports unlimited inline URL buttons attached to the welcome message
- Fully asynchronous using Aiogram 3.x and asyncpg
- Multi-group support with independent configuration
- Admin-only management commands
- HTML parse mode with placeholder support
- Broadcast system for all known chats
- Channel tracking system
- Structured logging
- Railway-ready deployment
- Fast and lightweight architecture

---

# 📜 Commands

| Command | Description |
|---|---|
| `/start` | Show main menu |
| `/set_welcome <text>` | Set the welcome message for this group |
| `/show_welcome` | Preview the current welcome message |
| `/del_welcome` | Delete the welcome message and all buttons |
| `/add_button <label> \| <url>` | Add an inline button |
| `/del_button <id>` | Delete a button by ID |
| `/list_buttons` | Show all buttons |
| `/add_channel` | Register a channel |
| `/del_channel <channel_id>` | Remove a channel |
| `/list_channels` | Show registered channels |
| `/broadcast` | Broadcast a message to all chats |
| `/stats` | Bot statistics |
| `/cancel` | Cancel current operation |

Management commands are restricted to administrators and group owners.

`/broadcast` is restricted to IDs listed in `BROADCAST_ADMIN_IDS`.

---

# 📝 Placeholders

Use these placeholders inside your welcome message.

| Placeholder | Description |
|---|---|
| `{name}` | New member full name |
| `{chat}` | Group name |

Example:

```text
/set_welcome Hello, {name}! Welcome to <b>{chat}</b> 🎉
```

---

# 🚀 Setup

## Local Development

1. Clone the repository.

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Copy environment file

```bash
cp .env.example .env
```

4. Configure your variables.

5. Run the bot

```bash
python bot.py
```

---

# 🚂 Railway Deployment

1. Create a Railway project.

2. Connect this repository.

3. Add the PostgreSQL plugin.

4. Set the following variables:

- BOT_TOKEN
- DATABASE_URL
- BROADCAST_ADMIN_IDS (Optional)

5. Deploy.

Railway will automatically use the included configuration files.

---

# ⚙ Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `BOT_TOKEN` | ✅ | — | Telegram Bot Token |
| `DATABASE_URL` | ✅ | — | PostgreSQL Connection URL |
| `BROADCAST_ADMIN_IDS` | ❌ | Empty | Telegram Admin IDs |
| `LOG_LEVEL` | ❌ | INFO | Logging Level |
| `TZ` | ❌ | UTC | Timezone |
| `MAX_CONCURRENT_TASKS` | ❌ | 2 | Broadcast Workers |
| `START_FROM_LATEST` | ❌ | true | Ignore queued updates |

---

# 📦 Requirements

- Python 3.12+
- aiogram 3.20.0
- asyncpg 0.30.0
- python-dotenv 1.2.2

---

# 🗄 Database

The bot uses PostgreSQL exclusively.

On first startup it automatically creates:

| Table | Purpose |
|---|---|
| `welcome_messages` | Welcome messages |
| `buttons` | Inline buttons |
| `channels` | Registered channels |
| `known_chats` | Broadcast targets |

No manual migrations are required.

---

# 👑 Developer

<p align="center">
<img src="https://i.postimg.cc/tgrqP2sW/IMG-20260620-133210-543.jpg" width="170">
</p>

<h2 align="center">Yousef Z. A. Shaheen 👑</h2>

<p align="center">
For contact 📩
</p>

<table align="center">

<tr>
<td>
<img src="https://i.postimg.cc/BbKNsJWZ/9ad79bcb73e8721663f873970d927b40.jpg" width="32">
</td>
<td>

**Instagram**

[@1.0_v_](https://instagram.com/1.0_v_)

</td>
</tr>

<tr>
<td>
<img src="https://i.postimg.cc/XJXQHwQ9/7cc98f0f748788604c632f6b5736a815.jpg" width="32">
</td>
<td>

**Telegram**

[@Y9_S4](https://t.me/Y9_S4)

</td>
</tr>

<tr>
<td>
<img src="https://i.postimg.cc/Z5F7CYWx/ff71e97414c40fc94af8e192ae16793a.jpg" width="32">
</td>
<td>

**WhatsApp**

https://wa.link/lc6f5w

</td>
</tr>

<tr>
<td>
<img src="https://i.postimg.cc/g0zMR9Rz/b2f532b8bf6aab51b8854971e4ddb210.jpg" width="32">
</td>
<td>

**TikTok**

[@zix8ii](https://www.tiktok.com/@zix8ii)

</td>
</tr>

<tr>
<td>
<img src="https://i.postimg.cc/prF917D8/a41e3010fda64b3bcf0589364926e040.jpg" width="32">
</td>
<td>

**Snapchat**

@fi1_oo

</td>
</tr>

<tr>
<td>
<img src="https://i.postimg.cc/tRZBFN1Z/73b610cbcd0296935a5849dbeccb7bdb.jpg" width="32">
</td>
<td>

**Facebook**

Yousef Z. Shaheen

</td>
</tr>

</table>

---

# 📄 License

MIT License

---

<p align="center">

⭐ If you like this project, don't forget to leave a star.

Made with ❤️ by <b>Yousef Z. A. Shaheen</b>

</p>
