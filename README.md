# MU-Portal-Automation-Bot

A Telegram bot that allows students of **Mizan-Tepi University eStudent Portal** to log in and access their academic transcript directly from Telegram.

The bot automates authentication to the university portal, maintains a session, scrapes academic data, calculates GPA, and returns formatted results to the user.

---

## 🚀 Features

- 🔐 Secure login using Student ID and Password  
- 📄 View Academic Transcript  
- 📊 Automatic GPA Calculation  
- 🧠 Session-based authentication  
- ✉️ Handles long Telegram messages safely  
- 🤖 Interactive menu system  

---

## 🛠️ Tech Stack

- **Python 3.10+**
- `python-telegram-bot` (v20+)
- `requests`
- `beautifulsoup4`
- Telegram Bot API

---

## 📁 Project Structure

```bash
.
├── mu_portal_bot.py
└── README.md
```

---

## ⚙️ How It Works

### 1️⃣ Authentication Process

1. User sends `/start`
2. Bot asks for:
   - Student ID
   - Password
3. Bot:
   - Loads login page
   - Extracts CSRF token
   - Sends login POST request
   - Stores authenticated session
4. Displays menu options

---

### 2️⃣ Transcript Retrieval

After successful login, the bot accesses:

```
https://estudent.mu.edu.et/estudent/student_profiles/show_transcript_to_student
```

The bot then:

- Parses transcript tables
- Extracts:
  - Course Code
  - Course Title
  - Grade
  - ECTS
  - Points
- Calculates:
  - Total ECTS
  - GPA
- Formats and sends transcript to Telegram

---

## 📦 Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/mu-portal-bot.git
cd mu-portal-bot
```

### Install Dependencies

```bash
pip install python-telegram-bot requests beautifulsoup4
```

---

## 🔑 Configuration

Open `mu_portal_bot.py` and replace:

```python
ApplicationBuilder().token("REPLACE THIS WITH YOUR TELEGRAM BOT TOKEN")
```

with your real Telegram Bot token:

```python
ApplicationBuilder().token("YOUR_REAL_BOT_TOKEN")
```

You can get a token from **@BotFather** on Telegram.

---

## ▶️ Run the Bot

```bash
python mu_portal_bot.py
```

The bot will start polling Telegram for updates.

---

## 💬 Usage

### Start Command

```
/start
```

### Menu Options (After Login)

```
1. Profile
2. Grades
3. Assessment Results
```

> ⚠️ Currently, only **Grades (Transcript)** is fully implemented.

---

## 📊 GPA Calculation

```
GPA = Total Points ÷ Total ECTS
```

The system:

- Ignores "Semester Total" rows  
- Ignores zero-credit courses  
- Groups courses by Year and Semester  
- Rounds GPA to two decimal places  

---

## ⚠️ Known Limitations

- Profile scraping not implemented  
- Assessment results not implemented  
- Portal HTML changes may break scraping  
- No database (session stored in memory only)  
- Credentials are not permanently stored  

---

## 🔐 Security Notice

- Uses session-based authentication  
- Does **NOT** permanently store credentials  
- Do **NOT** share your bot token publicly  

For production deployment:

- Use environment variables for tokens  
- Consider webhook mode  
- Add logging and error handling  

---

## 🌍 Deployment Options

You can deploy on:

- Railway  
- Render  
- PythonAnywhere  
- VPS (AWS, DigitalOcean, etc.)  
- Heroku  

---

## 🔮 Future Improvements

- Implement Profile scraping  
- Implement Assessment Results scraping  
- Add logout command  
- Add inline keyboard buttons  
- Add database support  
- Export transcript as PDF  
- Improve UI formatting  

---

## 👨‍💻 Author

**Malachi**

---

## 📜 License

This project is for educational purposes only.
