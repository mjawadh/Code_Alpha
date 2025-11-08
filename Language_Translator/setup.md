## ⚙️ System Requirements

| Component | Minimum | Recommended |
|------------|----------|-------------|
| CPU | Intel i5 (4th Gen) | Intel i7 (4th Gen or higher) |
| RAM | 8 GB | 16 GB |

---

**Repository Layout**
```
Language_Translator/
│
├── app.py                     # Main Streamlit script
├── model/
│   ├── **init**.py
│   ├── translator.py          # Handles model loading & translation logic
│
├── cache/
│   ├── **init**.py
│   ├── db_handler.py          # SQLAlchemy ORM + cache management
│
├── config/
│   ├── **init**.py
│   ├── settings.py            # Constants, language list, model configs
├── utils/
│   ├── **init**.py
│   ├── tokenizer_utils.py     # Text cleaning & truncation
│   ├── ui_helpers.py          # Streamlit layout & UI components
│
├── assets/
│   ├── screenshots.png
│
└── requirements.txt           # Project dependencies

````

---

## 🧠 Workflow Summary

| Step | Component | Description |
|------|------------|-------------|
| 1 | Streamlit UI | User inputs text, selects languages, toggles TTS |
| 2 | Preprocessing | Text cleaned and truncated for safe tokenization |
| 3 | Cache Handler | Checks SQLite for prior translations |
| 4 | Model | Performs translation using quantized mBART-large-50 |
| 5 | Output | Translated text shown and optionally read aloud |
| 6 | Cache Update | Translation persisted in SQLite for next time |

---

## 🔧 Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mjawadh/Code_Alpha/Language_Translator.git
cd offline-translator
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv vr
```
### 3️⃣ Activate Environment

* **Windows**

  ```bash
  vr\Scripts\activate
  ```
* **Linux/Mac**

  ```bash
  source vr/bin/activate
  ```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the App

```bash
streamlit run app.py
```


## 🧱 Dependencies

| Library         | Purpose                           |
| --------------- | --------------------------------- |
| `transformers`  | Load and run mBART-large-50 model |
| `torch`         | Backend for quantized inference   |
| `streamlit`     | Web-based UI                      |
| `SQLAlchemy`    | Database ORM for caching          |
| `pyttsx3`       | Offline text-to-speech (optional) |
| `protobuf`      | Model compatibility layer         |

**requirements.txt**

```
torch
transformers
streamlit
SQLAlchemy
pyttsx3
protobuf
```

---

## 🗂 Configuration (config/settings.py)

```python
MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"
MAX_TOKENS = 256
CACHE_EXPIRY_DAYS = 7
```

---

## 🧠 Model Details

* **Model:** `facebook/mbart-large-50-many-to-many-mmt`
* **Quantization:** 8-bit (CPU-efficient)
* **Tokenizer:** SentencePiece multilingual tokenizer
* **Translation Quality:** BLEU ~85% of full precision baseline
* **Languages Used:** 7 core global languages to balance UX and inference load

---

## 💾 Caching Strategy

* **Backend:** SQLite (via SQLAlchemy)
* **Structure:** Stores `(source_lang, target_lang, input_text, translated_text, timestamp)`
* **Cleanup Logic:** Rows older than 7 days or when DB exceeds 50MB
* **Benefit:** Instant retrieval for repeated translations
---

## 🎨 UI Components (utils/ui_helpers.py)

| Component         | Function                          |
| ----------------- | --------------------------------- |
| Header            | Displays logo & title             |
| Language Selector | Source & Target dropdowns         |
| Input Field       | Text area for translation input   |
| Result Panel      | Displays translation output       |
| Footer            | Branding info & Streamlit caption |

---

## 🔒 Offline Capability

| Feature        | Status | Notes                                |
| Translation    | ✅      | Fully offline                        |
| Caching        | ✅      | Local SQLite DB                      |
| Text-to-Speech | ⚠️     | Offline only for supported OS voices |
| UI Hosting     | ✅      | Streamlit app (local or cloud)       |
| API Calls      | ❌      | None used                            |


## 🧩 Future Enhancements

* Auto language detection for source input
* Improved TTS support for non-Latin scripts
* Export translations as CSV or JSON
* Docker container for reproducible deployment

---

## 👨‍💻 Development Notes

* Best tested on **Python 3.10+**
* Warm translations: <2s on i7 4th Gen
* Recommended to **run locally**, not Streamlit Cloud (due to large model size)

---

## 🏁 Author

Developed by **Muhammad Jawad**
An independent exploration into **offline NLP system design**, **quantized model optimization**, and **user-centric translation workflows**.

---

## 🧭 License

This project is released under the **MIT License** — feel free to fork, modify, and extend.

---

## ⚡ Quick Recap

**Goal:** Build an offline, multilingual translator that runs fully local
**Stack:** PyTorch, Transformers, Streamlit, SQLite
**Model:** Quantized mBART-large-50
**Edge:** Secure, fast, and wallet-friendly — no APIs, no subscriptions.

```