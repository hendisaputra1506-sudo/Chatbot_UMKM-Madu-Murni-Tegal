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
