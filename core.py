import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.4,
    api_key=os.getenv("GROQ_API_KEY")
)

BAD_WORDS = ["anjing","bangsat","kontol","memek","tolol","goblok"]

def contains_bad_word(text):
    return any(re.search(rf"\b{w}\b", text.lower()) for w in BAD_WORDS)

SYSTEM_CONTEXT = """
Anda adalah Customer Service UMKM *Madu Murni Tegal*.
Jawaban hanya seputar madu, pemesanan, dan pengiriman.
Gunakan bahasa WhatsApp yang ramah dan informatif.
"""

def get_bot_reply(text):
    text = text.strip()

    if text.lower() in ["halo","hai","hi","p","assalamualaikum"]:
        return (
            "Halo Kak 👋😊<br>"
            "Silakan tanya seputar <b>jenis madu</b>, <b>manfaat</b>, "
            "atau <b>cara pemesanan</b> 🍯"
        )

    if contains_bad_word(text):
        return "Mohon gunakan bahasa yang sopan ya Kak 🙏"

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_CONTEXT),
        ("human", "{input}")
    ])

    try:
        res = (prompt | llm).invoke({"input": text})
        return res.content
    except:
        return "⚠️ Sistem sedang bermasalah."