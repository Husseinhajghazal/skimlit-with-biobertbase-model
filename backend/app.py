from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tensorflow as tf
from transformers import AutoTokenizer, TFBertForSequenceClassification
import numpy as np
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

# Load model and tokenizer
model_dir = "skimlit_model"
model = TFBertForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

# Fix label mapping
model.config.id2label = {
    0: "BACKGROUND",
    1: "OBJECTIVE",
    2: "METHODS",
    3: "RESULTS",
    4: "CONCLUSIONS"
}
print("Model label mapping:", model.config.id2label)

@app.post("/summarize")
async def summarize(input: TextInput):
    sentences = sent_tokenize(input.text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    texts_with_pos = sentences
    encodings = tokenizer(texts_with_pos, truncation=True, padding=True, max_length=256, return_tensors='tf')
    
    dataset = tf.data.Dataset.from_tensor_slices(dict(encodings)).batch(len(texts_with_pos))
    predictions = model.predict(dataset)
    predicted_labels = np.argmax(predictions.logits, axis=-1)
    predicted_labels_decoded = [model.config.id2label.get(label, f"UNKNOWN_{label}") for label in predicted_labels]
    
    # Debug output
    print("Input sentences:", sentences)
    print("Predicted labels:", predicted_labels_decoded)
    print("Prediction probabilities:", tf.nn.softmax(predictions.logits, axis=-1).numpy())
    
    key_labels = ["OBJECTIVE", "RESULTS"]
    summary_sentences = [sentences[i] for i, label in enumerate(predicted_labels_decoded) if label in key_labels]
    
    if not summary_sentences:
        fallback_labels = ["METHODS", "CONCLUSIONS"]
        summary_sentences = [sentences[i] for i, label in enumerate(predicted_labels_decoded) if label in fallback_labels]
    
    if not summary_sentences:
        # Fallback to first and last sentence if no key labels
        if len(sentences) >= 2:
            summary_sentences = [sentences[0], sentences[-1]]
        elif sentences:
            summary_sentences = [sentences[0]]
    
    summary = " ".join(summary_sentences) if summary_sentences else "Unable to generate a summary from the provided text."
    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)