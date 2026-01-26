import axios from "axios";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ reply: "Method not allowed" });
  }

  let body = req.body;
  if (!body) {
    body = await new Promise(resolve => {
      let data = "";
      req.on("data", c => (data += c));
      req.on("end", () => resolve(JSON.parse(data)));
    });
  }

  const userMessage = body.message;

  if (!userMessage) {
    return res.json({ reply: "Silakan ketik pesan 😊" });
  }

  try {
    const ai = await axios.post(
      "https://api.groq.com/openai/v1/chat/completions",
      {
        model: "llama-3.1-8b-instant",
        messages: [{ role: "user", content: userMessage }],
        temperature: 0.4
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.GROQ_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );

    res.json({
      reply: ai.data.choices[0].message.content
    });

  } catch (err) {
    console.error("GROQ ERROR:", err.response?.data || err.message);
    res.json({ reply: "⚠️ Sistem sedang bermasalah." });
  }
}
