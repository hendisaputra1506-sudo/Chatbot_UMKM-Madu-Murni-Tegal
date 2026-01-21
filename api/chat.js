const { getBotReply } = require("../app/core.js")

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" })
  }

  try {
    const { message } = req.body
    const reply = await getBotReply(message)
    res.status(200).json({ reply })

  } catch (err) {
    console.error("API ERROR:", err.message)
    res.status(500).json({
      reply: "Maaf Kak, sistem sedang bermasalah 🙏"
    })
  }
}
