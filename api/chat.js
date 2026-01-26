import axios from "axios";

const BAD_WORDS = ["anjing", "bangsat", "kontol", "memek", "tolol", "goblok"];

function containsBadWord(text) {
  return BAD_WORDS.some(w => text.toLowerCase().includes(w));
}

function isGreeting(text) {
  return ["halo", "hai", "hi", "p", "assalamualaikum"].includes(
    text.toLowerCase().trim()
  );
}

export default async function handler(req, res) {

if (isGreeting(userMessage)) {
  return res.json({
    reply:
      "Halo Kak 👋😊\n" +
      "Ada yang bisa kami bantu terkait *produk madu*, *manfaat*, atau *cara pemesanan*?"
  });
}

  if (req.method !== "POST") {
    return res.status(405).json({ reply: "Method not allowed" });
  }

  const userMessage = req.body.message;

  if (!userMessage) {
    return res.json({ reply: "Silakan ketik pesan 😊" });
  }

  if (containsBadWord(userMessage)) {
    return res.json({ reply: "Mohon gunakan bahasa yang sopan ya Kak 🙏" });
  }

  const greetingRule = isGreeting(userMessage)
    ? "Awali dengan sapaan singkat."
    : "Langsung jawab tanpa sapaan.";

  const prompt = `
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
- ${greetingRule}

Pertanyaan:
"${userMessage}"
`;

  try {
    const ai = await axios.post(
      "https://api.groq.com/openai/v1/chat/completions",
      {
        model: "llama-3.1-8b-instant",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.4
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.GROQ_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );

    res.json({ reply: ai.data.choices[0].message.content });

  } catch (err) {
    res.json({ reply: "⚠️ Sistem sedang bermasalah." });
  }
}
