import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import *

LOGIN_URL = "https://estudent.mu.edu.et/auth/login"
GRADES_URL = "https://estudent.mu.edu.et/estudent/student_profiles/show_transcript_to_student"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["state"] = "USERNAME"
    await update.message.reply_text("Enter your student ID:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")

    if state == "USERNAME":
        context.user_data["username"] = update.message.text.strip()
        context.user_data["state"] = "PASSWORD"
        await update.message.reply_text("Enter your password:")

    elif state == "PASSWORD":
        context.user_data["password"] = update.message.text.strip()

        # store session login once
        session = login_session(
            context.user_data["username"],
            context.user_data["password"]
        )

        if not session:
            await update.message.reply_text("❌ Login failed.")
            context.user_data.clear()
            return

        context.user_data["session"] = session
        context.user_data["state"] = "MENU"

        await update.message.reply_text(
            "Choose an option:\n"
            "1️. Profile\n"
            "2️. Grades\n"
            "3️. Assessment Results\n\n"
        )
    elif state == "MENU":
        choice = update.message.text.strip()
        session = context.user_data["session"]

        if choice == "1":
            profile = fetch_profile(session)
            await send_long_message(update, profile)

        elif choice == "2":
            transcript = fetch_transcript(session)
            await send_long_message(update, transcript)

        elif choice == "3":
            assessments = fetch_assessments(session)
            await send_long_message(update, assessments)

        else:
            await update.message.reply_text("Please choose 1, 2, or 3.")


def login_session(USERNAME, PASSWORD):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": LOGIN_URL
    }

    session.get("https://estudent.mu.edu.et", headers=headers)
    login_page = session.get(LOGIN_URL, headers=headers)

    soup = BeautifulSoup(login_page.text, "html.parser")
    token = None

    token_input = soup.find("input", {"name": "_token"})
    if token_input:
        token = token_input["value"]
    if not token:
        meta = soup.find("meta", {"name": "csrf-token"})
        if meta:
           token = meta["content"]
        
    if not token:
        return "CSRF token not found."

    payload = {
        "user[user_name]": USERNAME,
        "user[password]": PASSWORD,
        "authenticity_token": token
    }

    login_response = session.post(LOGIN_URL, data=payload, headers=headers)

    if "login" in login_response.url.lower():
        return "Login failed. Check ID or password."

    return session


def fetch_profile(session):
    message = "Unavailable For Now!!"
    return message
def fetch_assessments(session):
    message = "Unavailable For Now!!"
    return message

def fetch_transcript(session):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": LOGIN_URL
    }
    grades_page = session.get(GRADES_URL, headers=headers)
    if grades_page.status_code != 200:
        return "Could not load transcript."

    soup = BeautifulSoup(grades_page.text, "html.parser")
    tables = soup.find_all("table")

    grades = []
    semester = 0

    for table in tables:
        semester += 1
        rows = table.find_all("tr")[1:]

        for row in rows:
            cols = [c.text.strip() for c in row.find_all("td")]
            if len(cols) < 6:
                continue
            if "Semester Total" in row.text or "Academic Status" in row.text:
                continue

            ects = float(cols[4]) if cols[6] else 0
            points = float(cols[6]) if cols[6] else 0

            grades.append({
                "code": cols[2],
                "title": cols[3],
                "grade": cols[5],
                "ects": ects,
                "points": points,
                "semester": semester
            })

    if not grades:
        return "No grades found."

    total_ects = sum(g["ects"] for g in grades)
    total_points = sum(g["points"] for g in grades)
    gpa = round(total_points / total_ects, 2) if total_ects else 0

    message = "*Academic Transcript*\n\n"
    current_sem = None

    for g in grades:
        if g["semester"] != current_sem and g["ects"] != 0:
            current_sem = g["semester"]
            year = (current_sem + 1) // 2
            sem = 2 if current_sem % 2 == 0 else 1
            message += f"\nYear {year} – Semester {sem}\n"
            message += "-" * 60 + "\n"

        if g["ects"] != 0:
            message += (
                f"{g['title']}\n"
                f"Grade: {g['grade']} \t|\t ECTS: {g['ects']}\n\n"
            )

    message += f"\n GPA: {gpa}\n"
    message += f"Total ECTS: {total_ects}"

    return message


async def send_long_message(update: Update, text: str):
    MAX = 4000
    for i in range(0, len(text), MAX):
        await update.message.reply_text(
            text[i:i+MAX],
            parse_mode="Markdown"
        )

def main():
    application = ApplicationBuilder().token("YOUR TOKEN").build()
    #You Need to Put in Your Telegram Bot Token For This to Work!!

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.run_polling()

if __name__ == "__main__":
    main()


