# EduMate AI Multi-Topic Chatbot

EduMate AI adalah chatbot edukasi berbasis AI/LLM yang dapat membantu pengguna belajar berbagai topik seperti Matematika, Sains, Sejarah, Bahasa, Teknologi, dan Umum.

## Use Case
**Education Bot / Asisten Belajar Multi-Topik**

Chatbot ini dirancang untuk:
- Menjawab pertanyaan pelajaran
- Menjelaskan konsep sulit
- Memberikan contoh soal
- Membuat rangkuman
- Memberikan rekomendasi belajar
- Menyesuaikan jawaban berdasarkan topik yang dipilih pengguna

## Fitur Utama
- UI chat modern
- Pilihan multi-topik:
  - Umum
  - Matematika
  - Sains
  - Sejarah
  - Bahasa Indonesia / Inggris
  - Teknologi
- Menggunakan OpenAI LLM jika API key tersedia
- Fallback rule-based jika API key belum tersedia
- Memory percakapan selama sesi
- Parameter kreatif: gaya santai, tutor, ramah, dan edukatif

## AI / NLP / LLM
Chatbot menggunakan OpenAI Chat Completions API sebagai model LLM untuk memproses bahasa alami dan memberikan respons yang relevan.

Jika `OPENAI_API_KEY` belum dipasang, chatbot tetap bisa berjalan menggunakan sistem fallback berbasis keyword.

## Struktur Project

```text
edumate_multi_topic/
├── app.py
├── config.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── README.md
```

## Cara Menjalankan Lokal

```bash
pip install -r requirements.txt
python app.py
```

Buka browser:

```text
http://127.0.0.1:5000
```

## Menjalankan dengan OpenAI API

### Windows PowerShell
```powershell
$env:OPENAI_API_KEY="isi_api_key_kamu"
python app.py
```

### Mac/Linux
```bash
export OPENAI_API_KEY="isi_api_key_kamu"
python app.py
```

## Deploy ke Render

1. Upload project ke GitHub.
2. Buka https://render.com
3. Klik New → Web Service.
4. Pilih repository GitHub.
5. Isi:
   - Build Command:
     ```bash
     pip install -r requirements.txt
     ```
   - Start Command:
     ```bash
     gunicorn app:app
     ```
6. Tambahkan Environment Variable:
   ```text
   OPENAI_API_KEY=isi_api_key_kamu
   ```
7. Klik Deploy.

## Contoh Pertanyaan

### Matematika
- Jelaskan persamaan linear satu variabel.
- Beri contoh soal luas lingkaran.

### Sains
- Jelaskan fotosintesis.
- Apa perbedaan gaya dan energi?

### Sejarah
- Buat rangkuman Revolusi Industri.
- Jelaskan penyebab Perang Dunia II.

### Bahasa
- Buat contoh kalimat pasif.
- Jelaskan perbedaan simple present dan present continuous.

### Teknologi
- Apa itu artificial intelligence?
- Jelaskan cara kerja internet secara sederhana.
