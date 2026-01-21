const axios = require("axios")

const GROQ_API_KEY = process.env.GROQ_API_KEY

async function getBotReply(userMessage = "") {
  if (!userMessage || userMessage.trim().length < 2) {
    return "Halo Kak 😊 ada yang bisa kami bantu?"
  }

  try {
    const response = await axios.post(
      "https://api.groq.com/openai/v1/chat/completions",
      {
        model: "llama-3.1-8b-instant",
        temperature: 0.4,
        messages: [
          {
            role: "system",
            content:
              "Anda adalah CS UMKM Madu Murni Tegal. Jawab singkat, ramah, dan sopan."
          },
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
    return "Maaf Kak, sistem sedang sibuk 🙏"
  }
}

module.exports = { getBotReply }
