# Brief Bot

## What the video to see how it works

[![Brief Bot](https://img.youtube.com/vi/DqRB0gNcvPs/1.jpg)](https://www.youtube.com/watch?v=DqRB0gNcvPs)

## Overview

Brief Bot Summarizer is a Chrome extension paired with a FastAPI backend that summarizes scientific texts, such as medical abstracts, by identifying key sentences (e.g., objectives, results). It leverages a BioBERT-based model to classify sentences, providing concise summaries for researchers and students. The extension features a user-friendly popup with a typewriter animation, spinner, and slide-in effects.

## Model Description

The backend uses a BioBERT model (`skimlit_model`), a transformer-based model pre-trained on biomedical texts (PubMed abstracts, PMC articles). Fine-tuned for sentence classification, it labels sentences as `BACKGROUND`, `OBJECTIVE`, `METHODS`, `RESULTS`, or `CONCLUSIONS`. The summarizer prioritizes `OBJECTIVE` and `RESULTS` sentences, falling back to `METHODS`, `CONCLUSIONS`, or the first and last sentences if needed.

## Prerequisites

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.11
- **Chrome Browser**: Latest version
- **Git**: For cloning the repository
- **Model**: BioBERT model (`skimlit_model`) directory (not included; see below)

## Setup Instructions (Local Usage)

### 1. Clone the Repository

```bash
git clone https://github.com/Husseinhajghazal/skimlit-with-biobertbase-model.git
cd skimlit-backend
```

### 2. Set Up the Backend

1. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK Data**:

   ```bash
   python -m nltk.downloader punkt_tab
   ```

4. **Obtain the BioBERT Model**:

   - The `skimlit_model` directory is not included due to size constraints.
   - You can download Skimlit_model.ipynb file and run it on collab, then download the skimlit_model from collab after the all cells runned successfully, or contact the repository owner for a compatible model.
   - Place the model in `backend/skimlit_model/`.

5. **Run the Backend**:
   ```bash
   python app.py
   ```
   - The FastAPI server runs at `http://localhost:8000`.

### 3. Set Up the Chrome Extension

1. **Download Extension Files**:

   - Obtain the extension files (not included in this repo):
     - `manifest.json`
     - `popup.html`
     - `popup.css`
     - `popup.js`
     - `background.js`
     - `icon128.png`
   - Place them in a directory (e.g., `skimlit_extension/`).

2. **Load the Extension**:
   - Open Chrome, go to `chrome://extensions/`.
   - Enable "Developer mode" (top-right).
   - Click "Load unpacked," select the `skimlit_extension/` directory.

### 4. Test the Summarizer

- Now time for test go for any medical article or paragraph, select it then right click and press summarize with brief bot

## Contributing

- Report issues or suggest features via GitHub Issues.
- Submit pull requests for improvements.

## License

MIT License

## Contact

For model access or support, contact [husseinghazal01@gmail.com].
