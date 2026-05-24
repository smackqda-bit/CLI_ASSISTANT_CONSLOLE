from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL")

if not API_KEY:
    raise ValueError("GROQ_API_KEY не найден в .env")

if not MODEL:
    raise ValueError("MODEL не задан в .env")
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

message_history = []
path = Path("chat_history.json")

if path.exists():
    message_history = json.loads(path.read_text(encoding="utf-8"))
else:
    message_history = []


def CLI(path, message_history):
    while True:
        message = input("Введите сообщение: ")
        if message.lower() in ["exit", "quit", "выход"]:
            path.write_text(
            json.dumps(message_history, ensure_ascii=False, indent=2),
            encoding="utf-8")

            logging.info("User exited program")
            break

        logging.info(f"User: {message}")
        message_history.append({"role": "user", "content": message})
        logging.info("Sending request to Groq...")
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=message_history,
                
            )
        except Exception as e:
            logging.error(f"API error: {e}")
            continue

        answer = response.choices[0].message.content
        logging.info(f"Assistant: {answer}")
        print("---")
        print(f"Ответ: {answer}")

        message_history.append({"role": "assistant", "content": answer})

        path.write_text(
            json.dumps(message_history, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        logging.info("Saving chat history to JSON")
        
        

CLI(path, message_history)