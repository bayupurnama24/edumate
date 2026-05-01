const chatBox = document.getElementById("chatBox");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const resetBtn = document.getElementById("resetBtn");
const topicSelect = document.getElementById("topicSelect");
const topicInfo = document.getElementById("topicInfo");
const exampleList = document.getElementById("exampleList");

const examples = {
    umum: [
        "Jelaskan cara belajar efektif",
        "Buat jadwal belajar sederhana",
        "Apa tips agar tidak mudah lupa?"
    ],
    matematika: [
        "Jelaskan persamaan linear",
        "Beri contoh soal luas lingkaran",
        "Bagaimana cara menghitung pecahan?"
    ],
    sains: [
        "Jelaskan fotosintesis",
        "Apa perbedaan gaya dan energi?",
        "Jelaskan rantai makanan"
    ],
    sejarah: [
        "Buat rangkuman Revolusi Industri",
        "Jelaskan penyebab Perang Dunia II",
        "Siapa tokoh penting Proklamasi Indonesia?"
    ],
    bahasa: [
        "Apa itu kalimat pasif?",
        "Buat contoh kalimat simple present",
        "Jelaskan perbedaan sinonim dan antonim"
    ],
    teknologi: [
        "Apa itu artificial intelligence?",
        "Jelaskan cara kerja internet",
        "Apa itu algoritma dalam pemrograman?"
    ]
};

function addMessage(text, sender) {
    const message = document.createElement("div");
    message.className = `message ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerText = text;

    message.appendChild(bubble);
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function updateTopicExamples() {
    const selectedTopic = topicSelect.value;
    const selectedText = topicSelect.options[topicSelect.selectedIndex].text;
    topicInfo.innerText = `Topik aktif: ${selectedText}`;

    exampleList.innerHTML = "";
    examples[selectedTopic].forEach((item) => {
        const li = document.createElement("li");
        li.innerText = item;
        exampleList.appendChild(li);
    });

    addMessage(`Topik diubah ke ${selectedText}. Silakan tanyakan materi yang ingin kamu pelajari.`, "bot");
}

topicSelect.addEventListener("change", updateTopicExamples);

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const userMessage = messageInput.value.trim();
    const selectedTopic = topicSelect.value;

    if (!userMessage) return;

    addMessage(userMessage, "user");
    messageInput.value = "";

    addMessage("Sedang berpikir...", "bot");
    const thinkingBubble = chatBox.lastChild.querySelector(".bubble");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: userMessage,
                topic: selectedTopic
            })
        });

        const data = await response.json();
        thinkingBubble.innerText = data.reply;
    } catch (error) {
        thinkingBubble.innerText = "Maaf, terjadi error saat menghubungi server.";
    }
});

resetBtn.addEventListener("click", async () => {
    await fetch("/reset", { method: "POST" });
    chatBox.innerHTML = "";
    addMessage("Memory sudah direset. Pilih topik lalu tanyakan materi yang ingin kamu pelajari.", "bot");
});
