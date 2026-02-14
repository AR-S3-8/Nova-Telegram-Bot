# Nova Telegram Bot 🤖

**Nova** is an interactive Telegram bot built with Python that allows users to manage accounts, reset passwords, deactivate accounts, view team information, and submit feedback. The bot uses inline keyboards and guided workflows for a smooth user experience.

---

## 🛠 Features

- **Main Menu & Interactive Navigation:** Navigate through bot functions using inline buttons.
- **Password Reset:** Secure password reset with email and OTP verification.
- **Account Deactivation:** Users can deactivate their account with confirmation steps.
- **Team Info:** Displays team members with contact and GitHub info.
- **Feedback Collection:** Users can submit feedback which is forwarded to a Telegram channel.
- **Project Overview:** Quick link to the project web application.

---

## ⚙️ Requirements

- Python **3.10+**
- Telegram bot token from [BotFather](https://t.me/BotFather)
- Dependencies in `requirements.txt`:

```bash
python-telegram-bot>=20.3
Note: Your requirements.txt should include all imported packages. For this bot, you can run pip freeze > requirements.txt after installing dependencies in your virtual environment.

🚀 Installation & Setup
Clone the repository:

git clone https://github.com/yourusername/nova-telegram-bot.git
cd nova-telegram-bot
Create a virtual environment:

python -m venv venv
Activate the virtual environment:

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
Install dependencies:

pip install -r requirements.txt
Configure bot token:

Replace the TOKEN variable in bot.py with your Telegram bot token.

(Optional) Use a .env file to store sensitive info.

Run the bot:

python bot.py
Start using:

Send /start in Telegram to begin interacting with the bot.

📁 Project Structure
nova-telegram-bot/
│
├─ bot.py               # Main bot code
├─ requirements.txt     # Python dependencies
├─ README.md            # Project documentation
└─ .gitignore           # Ignore files like venv and sensitive data

🔧 Notes
Conversations are managed with ConversationHandler.

Inline keyboards provide step-by-step guidance.

Feedback is sent to a dedicated Telegram channel.

Designed as a sample bot to demonstrate secure, interactive Telegram bot flows.