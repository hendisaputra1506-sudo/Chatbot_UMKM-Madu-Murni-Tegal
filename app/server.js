require("dotenv").config()
const express = require("express")
const path = require("path")
const { getBotReply } = require("./core")

const app = express()
const PORT = process.env.PORT || 3000

app.use(express.json())

// WEB CHATBOT
app.use(express.static(path.join(__dirname, "../public")))

// API CHAT
app.post("/chat", async (req, res) => {
  const { message } = req.body
  if (!message) {
    return res.json({ reply: "Pesan kosong." })
  }

  const reply = await getBotReply(message)
  res.json({ reply })
})

app.listen(PORT, () => {
  console.log("🚀 Server running on port", PORT)
})

// OPTIONAL: Start Telegram
require("./telegram")

// OPTIONAL: Start WA
require("../whatsapp/index")
