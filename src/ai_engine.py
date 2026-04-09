# Dành cho Agent/Thành viên: AI Engineer
# Lịch sử commit gợi ý: "feat: implement gemini triage engine with system prompt"

import streamlit as st
from openai import OpenAI
import json
import os
import io
from dotenv import load_dotenv

# Tải file .env
load_dotenv()

# Tải System Prompt từ file
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
try:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "You are a helpful medical assistant."

# Khởi tạo OpenAI Client (Tự động lấy OPENAI_API_KEY từ biến môi trường của dotenv)
client = OpenAI()

def get_triage_result(messages_list):
    try:
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if isinstance(messages_list, list):
            for msg in messages_list:
                api_messages.append({"role": msg["role"], "content": msg["content"]})
        else:
             api_messages.append({"role": "user", "content": messages_list})
             
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=api_messages,
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


def transcribe_audio_bytes(audio_bytes, language_code=None):
    try:
        # Chuẩn bị buffer âm thanh theo định dạng WebM (Chuẩn của Streamlit/Chrome)
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "input.webm"

        # Gọi Whisper-1 với tham số đơn giản nhất để đạt độ chính xác cao nhất
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            language="vi", 
            prompt="Bác sĩ ơi, tôi bị đau đầu."
        )
        return {"text": transcript.text.strip()}
    except Exception as e:
        return {"error": str(e)}
