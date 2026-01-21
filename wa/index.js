const {
    default: makeWASocket,
    useMultiFileAuthState
} = require("@whiskeysockets/baileys");

const axios = require("axios");
const Pino = require("pino");
const qrcode = require("qrcode-terminal");

// ✅ FUNGSI AMAN AMBIL TEKS
function getMessageText(msg) {
    if (!msg.message) return null;

    return (
    msg.message.conversation ||
    msg.message.extendedTextMessage?.text ||
    msg.message.imageMessage?.caption ||
    msg.message.videoMessage?.caption ||
    null
    );
}

async function startBot() {
console.log("🚀 Starting WhatsApp Bot");

const { state, saveCreds } = await useMultiFileAuthState("auth");

const sock = makeWASocket({
    auth: state,
    logger: Pino({ level: "silent" })
});

sock.ev.on("creds.update", saveCreds);

  // 🔗 CONNECTION
sock.ev.on("connection.update", (update) => {
    const { connection, qr } = update;

    if (qr) {
        console.log("📱 Scan QR Code:");
        qrcode.generate(qr, { small: true });
    }

    if (connection === "open") {
        console.log("✅ WhatsApp CONNECTED");
    }

    if (connection === "close") {
        console.log("❌ Connection closed, restarting...");
        startBot();
    }
});

  // 📩 MESSAGE HANDLER
sock.ev.on("messages.upsert", async ({ messages, type }) => {
if (type !== "notify") return

const msg = messages[0]
if (!msg || !msg.message || msg.key.fromMe) return

const jid = msg.key.remoteJid
const text = getMessageText(msg)
if (!text) return

console.log("📩 Pesan masuk:", text)

try {
    // ⌨️ Status mengetik
    await sock.sendPresenceUpdate("composing", jid)

    // ⏳ Delay alami (1.5 – 3 detik)
    const typingDelay = Math.floor(Math.random() * 1500) + 1500
    await delay(typingDelay)

    // 🔁 Kirim ke AI
    const res = await axios.post(
        "http://127.0.0.1:5000/chat",
        { message: text },
        { timeout: 15000 }
    )

    const reply =
        res.data?.reply ||
        "Maaf Kak, bisa dijelaskan sedikit lagi? 😊"

    // ⌨️ Simulasi ngetik lagi (opsional)
    await sock.sendPresenceUpdate("composing", jid)
    await delay(800)

    // 📤 Kirim pesan
    await sock.sendMessage(jid, { text: reply })

    // ⏸️ Berhenti mengetik
    await sock.sendPresenceUpdate("paused", jid)

    } catch (err) {
    console.error("❌ AI ERROR:", err.message)
    await sock.sendPresenceUpdate("paused", jid)
    await sock.sendMessage(jid, {
        text: "⚠️ Sistem sedang sibuk. Silakan coba lagi ya Kak 🙏"
    })
    }
})
}
function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

startBot();
