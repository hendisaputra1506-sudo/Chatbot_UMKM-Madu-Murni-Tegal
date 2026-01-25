import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# ===============================
# LOAD ENV
# ===============================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY belum di-set di .env")

# ===============================
# KONFIGURASI LLM
# ===============================
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.7,   # 🔥 lebih natural
    api_key=GROQ_API_KEY
)

# ===============================
# FILTER KATA KASAR
# ===============================
BAD_WORDS = [
    "anjing", "bangsat", "kontol", "memek",
    "tolol", "goblok", "ngentot", "asu"
]

def contains_bad_word(text: str) -> bool:
    text = text.lower()
    return any(re.search(rf"\b{w}\b", text) for w in BAD_WORDS)

# ===============================
# SYSTEM CONTEXT
# ===============================
SYSTEM_CONTEXT = """
Kamu adalah Customer Service resmi UMKM *Madu Murni Tegal*.

PROFIL:
- Berdiri sejak 2016
- Menjual madu murni alami
- Berbasis di Kota Tegal
- Produk dari peternak lebah mitra & ternak sendiri

JENIS MADU:
sengon, akasia, multiflora, rambutan, randu, pahit,
kelengkeng, kaliandra, hutan, klanceng, lawung,
madu anak, bawang, ketumbar organik, madu rumput.
Tersedia juga paket madu.

PEMESANAN:
- WhatsApp (utama)
- COD & pesan antar
- Kurir internal

PEMBAYARAN:
- Cash, Transfer, QRIS

GAYA JAWABAN:
- Bahasa santai, sopan, seperti admin WhatsApp
- Jawaban solutif & informatif
- Panjang jawaban sedang, tidak terlalu singkat atau panjang
- Gunakan *bold* hanya untuk info penting
- Jangan pakai HTML
- Jangan menyebut diri sebagai AI
- Jangan bertele-tele
"""

# ===============================
# FUNGSI UTAMA CHATBOT
# ===============================
def get_bot_reply(user_message: str) -> str:
    if not user_message or len(user_message.strip()) < 2:
        return "Halo Kak 😊 ada yang bisa kami bantu?"

    if contains_bad_word(user_message):
        return "Mohon gunakan bahasa yang sopan ya Kak 🙏 Kami siap bantu dengan senang hati."

    msg = user_message.lower()

    # ✅ salam lebih fleksibel
    is_greeting = any(s in msg for s in ["halo", "hai", "hi", "assalamualaikum", "pagi", "siang", "malam"])

    greeting_rule = (
        "Boleh awali jawaban dengan sapaan singkat dan ramah."
        if is_greeting
        else "Langsung jawab ke inti tanpa sapaan."
    )

    try:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                f"""{SYSTEM_CONTEXT}

ATURAN TAMBAHAN:
- {greeting_rule}
- Jika ditanya jam buka, alamat, atau cara pesan, jawab konsisten
"""
            ),
            ("human", "{input}")
        ])

        response = (prompt | llm).invoke({"input": user_message})

        # 🧹 post-processing ringan
        reply = response.content.strip()

        return reply

    except Exception as e:
        print("AI Error:", e)
        return "Maaf Kak, sistem sedang sibuk 🙏 Silakan coba lagi sebentar ya."
