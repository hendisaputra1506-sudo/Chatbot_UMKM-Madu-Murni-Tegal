const TelegramBot = require("node-telegram-bot-api")
const { getBotReply } = require("./core")

const bot = new TelegramBot(process.env.TELEGRAM_TOKEN, {
  polling: true
})

bot.on("message", async (msg) => {
  if (!msg.text) return
  const reply = await getBotReply(msg.text)
  bot.sendMessage(msg.chat.id, reply, { parse_mode: "HTML" })
})

console.log("🤖 Telegram bot running")
