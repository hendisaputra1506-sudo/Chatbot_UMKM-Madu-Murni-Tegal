import { getBotReply } from "../app/core.js"

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" })
  }

  try {
    const { message } = req.body

    if (!message) {
      return res.status(400).json({ reply: "Pesan kosong." })
    }

    const reply = await getBotReply(message)
    res.status(200).json({ reply })

  } catch (error) {
    console.error("API ERROR:", error.message)
    res.status(500).json({
      reply: "Maaf Kak, sistem sedang bermasalah 🙏"
    })
  }
}
