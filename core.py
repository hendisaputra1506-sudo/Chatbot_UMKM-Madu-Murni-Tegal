import os
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

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
    temperature=0.4,
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
# SYSTEM CONTEXT / TRAINING AI
# ===============================
SYSTEM_CONTEXT = """
Anda adalah Customer Service resmi UMKM bernama "Madu Murni Tegal".

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
- Cash
- Transfer
- QRIS

ATURAN JAWABAN:
1. Bahasa santai & sopan (WhatsApp style)
2. Jawaban singkat, jelas, to the point
3. Gunakan *bold* untuk info penting
4. Dilarang HTML & Markdown lain
5. Jangan menyebut diri sebagai AI
6. Fokus madu, manfaat, harga, pengiriman
"""

# ===============================
# FUNGSI UTAMA CHATBOT
# ===============================
def get_bot_reply(user_message: str) -> str:
    if not user_message or len(user_message.strip()) < 2:
        return "Halo Kak 😊 ada yang bisa kami bantu?"

    if contains_bad_word(user_message):
        return "Mohon gunakan bahasa yang sopan ya Kak 🙏"

    salam = ["halo", "hai", "hi", "p", "assalamualaikum"]
    is_greeting = user_message.lower().strip() in salam

    sapaan_rule = (
        "Awali jawaban dengan sapaan singkat."
        if is_greeting
        else "Langsung jawab ke inti tanpa sapaan."
    )

    try:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                f"""{SYSTEM_CONTEXT}

TAMBAHAN:
- {sapaan_rule}
"""
            ),
            ("human", "{input}")
        ])

        response = (prompt | llm).invoke({"input": user_message})
        return response.content.strip()

    except Exception as e:
        print("AI Error:", e)
        return "Maaf Kak, sistem sedang sibuk 🙏"
