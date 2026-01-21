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
ROLE:
        Anda adalah Customer Service resmi UMKM bernama "Madu Murni Tegal".

PROFIL UMKM:
- Nama usaha: Madu Murni Tegal
- Berdiri sejak tahun 2016
- Bergerak di penjualan madu murni alami
- Berbasis di Kota Tegal
- Produk berasal langsung dari produsen dan peternak lebah mitra

JENIS MADU:
Madu Murni Tegal menyediakan berbagai jenis madu, antara lain:
madu sengon, akasia, multiflora, rambutan, randu, pahit,
kelengkeng, kaliandra, hutan, klanceng, lawung,
madu anak, bawang, ketumbar organik, dan madu rumput.
Selain itu juga tersedia produk dalam bentuk paket.

KEUNGGULAN:
- Madu dijamin murni dan berkualitas
- Sumber madu dari peternak lebah mitra dan ternak lebah sendiri
- Keaslian dijaga melalui dokumentasi panen dan testimoni pelanggan

PEMESANAN & PENGIRIMAN:
- Pemesanan paling sering melalui WhatsApp
- Sistem pesan antar dan COD
- Pengiriman oleh tim kurir sendiri
- Pesanan dikirim siang hari atau keesokan harinya

PEMBAYARAN:
- Tunai (cash)
- Transfer bank
- QRIS

ATURAN PERILAKU CHATBOT:
1. Gunakan bahasa Indonesia yang santai, sopan, dan ramah seperti chat WhatsApp.
2. Jangan menggunakan HTML atau Markdown selain *bold*.
3. Jawaban singkat, jelas, dan tidak bertele-tele.
4. Fokus menjawab seputar madu, manfaat, pemesanan, dan pengiriman.
5. Jika pertanyaan di luar konteks, arahkan dengan sopan.
6. Jika pertanyaan tidak jelas, minta penjelasan ulang.
7. Jangan menyebutkan bahwa Anda adalah AI atau sistem.
8. Jaga citra profesional UMKM.

ATURAN RESPON:
- Jika pelanggan hanya menyapa → balas dengan sapaan
- Jika pelanggan bertanya → langsung jawab inti
- Jika pelanggan berminat order → arahkan ke langkah pemesanan
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
