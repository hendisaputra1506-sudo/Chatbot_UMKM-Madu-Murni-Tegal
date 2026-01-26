const axios = require("axios")

const GROQ_API_KEY = process.env.GROQ_API_KEY
if (!GROQ_API_KEY) {
  throw new Error("GROQ_API_KEY belum di-set")
}

/* ===============================
   FILTER KATA KASAR
================================ */
const BAD_WORDS = [
  "anjing", "bangsat", "kontol", "memek",
  "tolol", "goblok", "ngentot", "asu"
]

function containsBadWord(text = "") {
  const lower = text.toLowerCase()
  return BAD_WORDS.some(word =>
    new RegExp(`\\b${word}\\b`, "i").test(lower)
  )
}

/* ===============================
   SYSTEM CONTEXT
================================ */
const SYSTEM_CONTEXT = `
ROLE:
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
`

/* ===============================
   FUNGSI UTAMA
================================ */
async function getBotReply(userMessage = "") {
  if (!userMessage || userMessage.trim().length < 2) {
    return "Halo Kak 😊 ada yang bisa kami bantu?"
  }

  if (containsBadWord(userMessage)) {
    return "Mohon gunakan bahasa yang sopan ya Kak 🙏"
  }

  try {
    const response = await axios.post(
      "https://api.groq.com/openai/v1/chat/completions",
      {
        model: "llama-3.1-8b-instant",
        temperature: 0.4,
        messages: [
          { role: "system", content: SYSTEM_CONTEXT },
          { role: "user", content: userMessage }
        ]
      },
      {
        headers: {
          Authorization: `Bearer ${GROQ_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    )

    return response.data.choices[0].message.content.trim()

  } catch (err) {
    console.error("AI ERROR:", err.message)
    return "Maaf Kak, sistem sedang bermasalah 🙏"
  }
}

module.exports = { getBotReply }
