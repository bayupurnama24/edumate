import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from config import BOT_CONFIG, SYSTEM_PROMPT, TOPIC_PROMPTS

load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

conversation_memory = []


def fallback_response(user_message: str, topic: str) -> str:
    text = user_message.lower()
    topic = topic.lower()

    if any(word in text for word in ["halo", "hai", "hello"]):
        return f"Halo! Aku EduMate AI. Kamu sedang memilih topik {topic.title()}. Mau belajar apa hari ini?"

    if topic == "matematika":
        if "lingkaran" in text:
            return "Luas lingkaran dihitung dengan rumus L = π × r². Contoh: jika jari-jari 7 cm, maka L = 22/7 × 7² = 154 cm²."
        if "persamaan" in text:
            return "Persamaan linear satu variabel adalah persamaan dengan satu variabel berpangkat satu. Contoh: 2x + 4 = 10, maka 2x = 6, jadi x = 3."
        return "Untuk Matematika, kirim soal atau topiknya. Aku bisa bantu langkah-langkahnya, misalnya aljabar, bangun datar, pecahan, atau peluang."

    if topic == "sains":
        if "fotosintesis" in text:
            return "Fotosintesis adalah proses tumbuhan membuat makanan sendiri dengan bantuan cahaya matahari. Bahan: air, karbon dioksida, dan cahaya. Hasil: glukosa dan oksigen."
        if "energi" in text:
            return "Energi adalah kemampuan untuk melakukan kerja. Contohnya energi panas, energi cahaya, energi gerak, dan energi listrik."
        return "Untuk Sains, aku bisa bantu menjelaskan biologi, fisika, kimia, lingkungan, atau konsep ilmiah sehari-hari."

    if topic == "sejarah":
        if "revolusi industri" in text:
            return "Revolusi Industri adalah perubahan besar dari produksi manual menjadi produksi menggunakan mesin. Dimulai di Inggris pada abad ke-18 dan berdampak pada ekonomi, transportasi, dan kehidupan sosial."
        if "perang dunia" in text:
            return "Perang Dunia II terjadi pada 1939–1945. Penyebabnya antara lain ekspansi Nazi Jerman, fasisme, krisis ekonomi, dan kegagalan diplomasi internasional."
        return "Untuk Sejarah, aku bisa bantu menjelaskan tokoh, peristiwa, kronologi, sebab-akibat, dan dampaknya."

    if topic == "bahasa":
        if "kalimat pasif" in text:
            return "Kalimat pasif adalah kalimat yang subjeknya dikenai tindakan. Contoh: 'Buku itu dibaca oleh Rani.'"
        if "simple present" in text:
            return "Simple present digunakan untuk kebiasaan atau fakta umum. Contoh: 'I study every day.'"
        return "Untuk Bahasa, aku bisa bantu tata bahasa, contoh kalimat, kosakata, terjemahan sederhana, dan struktur paragraf."

    if topic == "teknologi":
        if "ai" in text or "artificial intelligence" in text:
            return "AI atau Artificial Intelligence adalah teknologi yang membuat komputer dapat meniru kemampuan manusia seperti memahami bahasa, mengenali gambar, dan memberi rekomendasi."
        if "internet" in text:
            return "Internet adalah jaringan global yang menghubungkan banyak komputer. Saat kamu membuka website, perangkatmu mengirim permintaan ke server lalu menerima data untuk ditampilkan."
        return "Untuk Teknologi, aku bisa bantu menjelaskan AI, komputer, internet, coding, aplikasi, dan keamanan digital."

    if "rangkuman" in text or "ringkas" in text:
        return "Bisa. Kirim teks atau topik yang ingin dirangkum, nanti aku buatkan versi singkat dan mudah dipahami."

    return "Aku bisa bantu berbagai topik. Pilih topik di sebelah kiri, lalu tanyakan materi yang ingin kamu pahami."


def generate_ai_response(user_message: str, topic: str) -> str:
    global conversation_memory

    topic_instruction = TOPIC_PROMPTS.get(topic, TOPIC_PROMPTS["umum"])

    conversation_memory.append({
        "role": "user",
        "content": f"Topik yang dipilih: {topic}. Pertanyaan pengguna: {user_message}"
    })
    conversation_memory = conversation_memory[-BOT_CONFIG["max_history"]:]

    if not client:
        bot_reply = fallback_response(user_message, topic)
        conversation_memory.append({"role": "assistant", "content": bot_reply})
        return bot_reply

    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": topic_instruction},
        ] + conversation_memory

        response = client.chat.completions.create(
            model=BOT_CONFIG["model"],
            messages=messages,
            temperature=BOT_CONFIG["temperature"],
            max_tokens=650,
        )

        bot_reply = response.choices[0].message.content
        conversation_memory.append({"role": "assistant", "content": bot_reply})
        conversation_memory = conversation_memory[-BOT_CONFIG["max_history"]:]
        return bot_reply

    except Exception:
        return (
            "Maaf, mode AI sedang bermasalah. Untuk sementara aku jawab dengan mode fallback.\n\n"
            + fallback_response(user_message, topic)
        )


@app.route("/")
def index():
    return render_template("index.html", config=BOT_CONFIG)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    topic = data.get("topic", "umum").strip().lower()

    if not user_message:
        return jsonify({"reply": "Tulis pertanyaan dulu ya 😊"})

    reply = generate_ai_response(user_message, topic)
    return jsonify({"reply": reply})


@app.route("/reset", methods=["POST"])
def reset():
    global conversation_memory
    conversation_memory = []
    return jsonify({"status": "success", "message": "Memory percakapan sudah dihapus."})


if __name__ == "__main__":
    app.run(debug=True)
